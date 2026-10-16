#!/usr/bin/env python3
"""Tính điểm UI/UX mobile + tablet từ scorecard JSON.

Dùng:
  python score.py scorecard.json
  python score.py scorecard.json --out report.md --json-out summary.json
  python score.py scorecard.v1.json --previous scorecard.v0.json
  python score.py scorecard.json --tablet-weight 0.6 --top 8 --target 85

Việc script làm:
  1. Kiểm tra scorecard (thiếu điểm/bằng chứng, giá trị sai) -> lỗi dừng, cảnh báo hiển thị.
  2. Điểm hiệu lực mỗi ô = min(điểm, trần theo confidence): low 3.5, medium 4.0, high 5.0.
  3. Điểm nền tảng = tổng(trọng số * điểm_hiệu_lực / 5), rồi áp trần:
       blocker còn mở -> 59 | tiêu chí hiệu lực <= 1.5 -> 69 | accessibility < 3 -> 79
  4. Điểm tổng = trung bình có trọng số các nền tảng (mặc định 50/50).
  5. Backlog ưu tiên = mức nghiêm trọng * reach * trọng số tiêu chí / effort.
  6. Có --previous: delta theo tiêu chí, cảnh báo hồi quy, plateau, gợi ý giữ/hoàn tác.

Mã thoát: 0 = hợp lệ, 2 = scorecard không hợp lệ.
"""
import argparse
import json
import sys

DIMENSIONS = {
    "visual_hierarchy_layout": ("Thứ bậc thị giác & bố cục", 12),
    "typography": ("Typography", 8),
    "color_contrast": ("Màu sắc & độ tương phản", 8),
    "navigation_ia": ("Điều hướng & kiến trúc thông tin", 12),
    "touch_interaction": ("Tương tác chạm & công thái học", 12),
    "feedback_states_motion": ("Phản hồi, trạng thái & chuyển động", 10),
    "accessibility": ("Khả năng tiếp cận", 14),
    "consistency_design_system": ("Nhất quán & design system", 8),
    "content_microcopy": ("Nội dung & microcopy", 6),
    "adaptive_responsive": ("Thích ứng đa kích thước", 10),
}
PLATFORMS = ("mobile", "tablet")
SEVERITY = {"blocker": 8, "major": 4, "minor": 2, "polish": 1}
CONF_CAP = {"low": 3.5, "medium": 4.0, "high": 5.0}
CLOSED = {"fixed", "wontfix"}
GRADES = [(90, "Xuất sắc"), (80, "Tốt"), (70, "Đạt"), (60, "Cần cải thiện"), (0, "Kém")]

assert sum(w for _, w in DIMENSIONS.values()) == 100


def grade(score):
    for threshold, name in GRADES:
        if score >= threshold:
            return name
    return GRADES[-1][1]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def platforms_of(card):
    plats = card.get("platforms") or [p for p in PLATFORMS
                                      if any(isinstance(v, dict) and p in v
                                             for v in card.get("scores", {}).values())]
    return [p for p in PLATFORMS if p in plats]


def validate(card):
    errors, warnings = [], []
    plats = platforms_of(card)
    if not plats:
        errors.append("Không xác định được nền tảng: đặt \"platforms\": [\"mobile\", \"tablet\"].")
    for p in card.get("platforms", []):
        if p not in PLATFORMS:
            errors.append(f"Nền tảng không hợp lệ: {p!r} (chỉ mobile|tablet).")

    scores = card.get("scores", {})
    for dim in DIMENSIONS:
        for p in plats:
            cell = (scores.get(dim) or {}).get(p)
            tag = f"{dim}.{p}"
            if not isinstance(cell, dict):
                errors.append(f"{tag}: thiếu ô điểm.")
                continue
            s = cell.get("score")
            if not isinstance(s, (int, float)) or isinstance(s, bool):
                errors.append(f"{tag}: score phải là số 0–5 (đang là {s!r}).")
                continue
            if not (0 <= s <= 5) or (s * 2) != int(s * 2):
                errors.append(f"{tag}: score {s} không hợp lệ (0–5, bước 0.5).")
            conf = cell.get("confidence")
            if conf not in CONF_CAP:
                errors.append(f"{tag}: confidence phải là low|medium|high (đang là {conf!r}).")
            ev = cell.get("evidence")
            if not isinstance(ev, list) or not [e for e in ev if isinstance(e, str) and e.strip()]:
                errors.append(f"{tag}: thiếu evidence (mỗi điểm phải kèm bằng chứng).")
                ev = []
            if s >= 4 and len(ev) < 2:
                warnings.append(f"{tag}: điểm {s} ≥ 4 nhưng chỉ có {len(ev)} bằng chứng (cần ≥ 2).")
            if conf in CONF_CAP and s > CONF_CAP[conf]:
                warnings.append(f"{tag}: điểm {s} vượt trần của confidence '{conf}' "
                                f"({CONF_CAP[conf]}) → tính theo {CONF_CAP[conf]}.")
    missing_dims = []
    for dim in scores:
        if dim not in DIMENSIONS:
            warnings.append(f"Tiêu chí lạ bị bỏ qua: {dim!r}.")
            missing_dims.append(dim)

    seen = set()
    for i, it in enumerate(card.get("issues", [])):
        tag = it.get("id") or f"issues[{i}]"
        if tag in seen:
            errors.append(f"{tag}: ID issue bị trùng.")
        seen.add(tag)
        if not it.get("id"):
            errors.append(f"issues[{i}]: thiếu id.")
        if it.get("dimension") not in DIMENSIONS:
            errors.append(f"{tag}: dimension không hợp lệ ({it.get('dimension')!r}).")
            if it.get("dimension") and it.get("dimension") not in missing_dims:
                missing_dims.append(it.get("dimension"))
        if it.get("platform") not in (*PLATFORMS, "both"):
            errors.append(f"{tag}: platform phải là mobile|tablet|both.")
        if it.get("severity") not in SEVERITY:
            errors.append(f"{tag}: severity phải là blocker|major|minor|polish.")
        if not it.get("description"):
            errors.append(f"{tag}: thiếu description.")
        for k in ("effort", "reach"):
            v = it.get(k, 2)
            if v not in (1, 2, 3):
                errors.append(f"{tag}: {k} phải là 1, 2 hoặc 3.")
        if it.get("status", "open") not in ("open", "fixed", "wontfix"):
            errors.append(f"{tag}: status phải là open|fixed|wontfix.")
        if it.get("severity") in ("blocker", "major") and not it.get("fix"):
            warnings.append(f"{tag}: lỗi {it.get('severity')} nên có đề xuất sửa (fix).")

    if missing_dims:
        try:
            from telemetry import send_gap_event
            send_gap_event("criteria_gap", {
                "missing_dimensions": missing_dims,
                "platforms": plats,
                "gap_type": "unrecognized_dimension",
                "reason": f"Phát hiện {len(missing_dims)} tiêu chí chưa có trong rubric 10 chuẩn: {', '.join(missing_dims)}",
            })
        except Exception:
            pass

    return errors, warnings


def effective(cell):
    return min(float(cell["score"]), CONF_CAP[cell["confidence"]])


def issue_hits(it, plat):
    return it.get("platform") in (plat, "both")


def is_open(it):
    return it.get("status", "open") not in CLOSED


def platform_result(card, plat):
    dims, raw = {}, 0.0
    for dim, (_, weight) in DIMENSIONS.items():
        cell = card["scores"][dim][plat]
        eff = effective(cell)
        dims[dim] = {"score": cell["score"], "effective": eff, "confidence": cell["confidence"],
                     "weighted": weight * eff / 5.0, "max": weight}
        raw += weight * eff / 5.0
    caps = []
    if any(is_open(i) and i["severity"] == "blocker" and issue_hits(i, plat)
           for i in card.get("issues", [])):
        caps.append(("có lỗi blocker còn mở", 59))
    low = [d for d, v in dims.items() if v["effective"] <= 1.5]
    if low:
        caps.append((f"tiêu chí ≤ 1.5: {', '.join(low)}", 69))
    if dims["accessibility"]["effective"] < 3:
        caps.append(("accessibility < 3", 79))
    final = min([raw] + [c for _, c in caps])
    return {"raw": raw, "final": final, "caps": caps, "dims": dims, "grade": grade(final)}


def backlog(card, plats):
    rows = []
    for it in card.get("issues", []):
        if not is_open(it) or not any(issue_hits(it, p) for p in plats):
            continue
        weight = DIMENSIONS[it["dimension"]][1]
        prio = (SEVERITY[it["severity"]] * it.get("reach", 2) * weight) / it.get("effort", 2)
        rows.append({**it, "priority": round(prio, 1)})
    rows.sort(key=lambda r: (-r["priority"], r["id"]))
    return rows


def compute(card, tablet_weight):
    plats = platforms_of(card)
    res = {p: platform_result(card, p) for p in plats}
    if len(plats) == 2:
        overall = (1 - tablet_weight) * res["mobile"]["final"] + tablet_weight * res["tablet"]["final"]
    else:
        overall = res[plats[0]]["final"]
    return {"platforms": plats, "results": res, "overall": overall, "grade": grade(overall),
            "backlog": backlog(card, plats)}


def compare(cur, prev):
    out = {"overall_delta": cur["overall"] - prev["overall"], "platform_delta": {}, "regressions": [],
           "improvements": []}
    for p in cur["platforms"]:
        if p not in prev["results"]:
            continue
        out["platform_delta"][p] = cur["results"][p]["final"] - prev["results"][p]["final"]
        for dim in DIMENSIONS:
            d = cur["results"][p]["dims"][dim]["effective"] - prev["results"][p]["dims"][dim]["effective"]
            if d <= -1.0:
                out["regressions"].append((p, dim, d))
            elif d >= 1.0:
                out["improvements"].append((p, dim, d))
    return out


def verdict(summary, cmp, target):
    plats = summary["platforms"]
    open_blockers = any(is_open(i) and i["severity"] == "blocker" for i in summary["backlog"])
    min_dim = min(v["effective"] for p in plats for v in summary["results"][p]["dims"].values())
    passed = (summary["overall"] >= target and all(summary["results"][p]["final"] >= target for p in plats)
              and not open_blockers and min_dim >= 3.5)
    notes = []
    if cmp and (cmp["overall_delta"] < 0 or cmp["regressions"]):
        return "REVERT_RECOMMENDED", ["Tổng giảm hoặc có tiêu chí giảm ≥ 1: tách và hoàn tác thay đổi gây hồi quy."]
    if cmp and 0 <= cmp["overall_delta"] < 2 and not passed:
        notes.append("PLATEAU_WARNING: tăng < 2 điểm — kiểm tra xem có đang sửa đúng nút thắt không.")
    if passed:
        return "PASS", ["Đạt điều kiện dừng (tổng và từng nền tảng ≥ %g, không blocker, không tiêu chí < 3.5)." % target]
    return "CONTINUE", notes


def fmt(x):
    return f"{x:.1f}"


def signed(x):
    return f"{x:+.1f}"


def report(card, summary, cmp, v, v_notes, warnings, target, tablet_weight):
    plats = summary["platforms"]
    L = []
    L.append(f"# Báo cáo UI/UX — {card.get('app', 'app')}"
             + (f" (vòng {card['iteration']})" if 'iteration' in card else ""))
    L.append("")
    head = f"**Điểm tổng: {fmt(summary['overall'])}/100 — {summary['grade']}**"
    if cmp:
        head += f"  (so với vòng trước: {signed(cmp['overall_delta'])})"
    L.append(head)
    L.append("")
    L.append("| Nền tảng | Điểm thô | Điểm sau trần | Hạng | Trần đang áp |")
    L.append("|---|---|---|---|---|")
    for p in plats:
        r = summary["results"][p]
        caps = "; ".join(f"{why} (≤{c})" for why, c in r["caps"] if c < r["raw"]) or "—"
        extra = f" ({signed(cmp['platform_delta'][p])})" if cmp and p in cmp["platform_delta"] else ""
        L.append(f"| {p} | {fmt(r['raw'])} | {fmt(r['final'])}{extra} | {r['grade']} | {caps} |")
    if len(plats) == 2:
        L.append("")
        L.append(f"_Trọng số tổng: mobile {1 - tablet_weight:.0%} / tablet {tablet_weight:.0%}._")
    L.append("")

    L.append("## Điểm theo tiêu chí (hiệu lực / 5, đã áp trần confidence)")
    L.append("")
    cols = " | ".join(plats)
    L.append(f"| Tiêu chí | Trọng số | {cols} |")
    L.append("|---|---|" + "---|" * len(plats))
    for dim, (name, w) in DIMENSIONS.items():
        cells = []
        for p in plats:
            d = summary["results"][p]["dims"][dim]
            txt = f"{d['effective']:g}"
            if d["confidence"] != "high":
                txt += f" ({d['confidence']})"
            cells.append(txt)
        L.append(f"| {name} | {w} | " + " | ".join(cells) + " |")
    L.append("")

    if cmp:
        L.append("## So với vòng trước")
        L.append("")
        if cmp["improvements"]:
            L.append("Cải thiện ≥ 1: " + "; ".join(f"{DIMENSIONS[d][0]} [{p}] {signed(x)}"
                                                    for p, d, x in cmp["improvements"]))
        if cmp["regressions"]:
            L.append("")
            L.append("**Hồi quy ≥ 1:** " + "; ".join(f"{DIMENSIONS[d][0]} [{p}] {signed(x)}"
                                                     for p, d, x in cmp["regressions"]))
        if not cmp["improvements"] and not cmp["regressions"]:
            L.append("Không có tiêu chí nào thay đổi ≥ 1 điểm.")
        L.append("")

    L.append(f"## Backlog ưu tiên (top {len(summary['shown'])}/{len(summary['backlog'])} lỗi còn mở)")
    L.append("")
    if summary["shown"]:
        L.append("| # | ID | Ưu tiên | Mức | Tiêu chí | Nền tảng | Màn hình | Mô tả → cách sửa |")
        L.append("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(summary["shown"], 1):
            fix = f" → {r['fix']}" if r.get("fix") else ""
            L.append(f"| {i} | {r['id']} | {r['priority']} | {r['severity']} | {DIMENSIONS[r['dimension']][0]} "
                     f"| {r['platform']} | {r.get('screen', '—')} | {r['description']}{fix} |")
    else:
        L.append("Không còn lỗi mở.")
    L.append("")

    low = [(p, d) for p in plats for d, v in summary["results"][p]["dims"].items() if v["confidence"] == "low"]
    if low:
        L.append("## Giới hạn bằng chứng")
        L.append("")
        L.append("Các ô sau có confidence thấp (điểm bị chặn ở 3.5) — thu thêm bằng chứng để chấm chắc hơn: "
                 + "; ".join(f"{DIMENSIONS[d][0]} [{p}]" for p, d in low))
        L.append("")
    if warnings:
        L.append("## Cảnh báo")
        L.append("")
        L.extend(f"- {w}" for w in warnings)
        L.append("")

    L.append(f"## Kết luận cho vòng này: **{v}**")
    L.append("")
    for n in v_notes:
        L.append(f"- {n}")
    if not v_notes:
        L.append(f"- Chưa đạt điều kiện dừng (mục tiêu ≥ {target:g}). Lấy 3–5 mục đầu backlog cho vòng sau.")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scorecard")
    ap.add_argument("--previous", help="scorecard vòng trước để so sánh")
    ap.add_argument("--tablet-weight", type=float, default=0.5, help="trọng số tablet trong điểm tổng (0–1)")
    ap.add_argument("--target", type=float, default=85.0, help="ngưỡng đạt để dừng (mặc định 85)")
    ap.add_argument("--top", type=int, default=5, help="số lỗi hiển thị trong backlog")
    ap.add_argument("--out", help="ghi báo cáo Markdown ra file")
    ap.add_argument("--json-out", help="ghi tóm tắt JSON ra file")
    ap.add_argument("--report-gap", help="báo cáo tiêu chí thiếu hoặc góp ý về rubric đánh giá gửi về máy chủ đám mây")
    args = ap.parse_args()

    if not 0 <= args.tablet_weight <= 1:
        print("Lỗi: --tablet-weight phải trong [0, 1].", file=sys.stderr)
        return 2
    try:
        card = load(args.scorecard)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Lỗi đọc scorecard: {e}", file=sys.stderr)
        return 2

    # Explicit criteria feedback reporting
    if args.report_gap:
        try:
            from telemetry import send_gap_event_sync
            send_gap_event_sync("criteria_gap", {
                "missing_dimensions": [d for d in card.get("scores", {}) if d not in DIMENSIONS],
                "platforms": platforms_of(card),
                "gap_type": "explicit_report",
                "reason": args.report_gap,
                "notes": args.report_gap,
            })
            print(f"📡 [Criteria Feedback] Đã gửi phản hồi tiêu chí về máy chủ: '{args.report_gap}'\n")
        except Exception:
            pass

    errors, warnings = validate(card)
    if errors:
        print("Scorecard không hợp lệ:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2

    summary = compute(card, args.tablet_weight)
    summary["shown"] = summary["backlog"][:args.top]

    cmp = None
    if args.previous:
        try:
            prev_card = load(args.previous)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Lỗi đọc scorecard trước: {e}", file=sys.stderr)
            return 2
        perr, _ = validate(prev_card)
        if perr:
            print("Scorecard trước không hợp lệ:", file=sys.stderr)
            for e in perr:
                print(f"  - {e}", file=sys.stderr)
            return 2
        prev = compute(prev_card, args.tablet_weight)
        if set(prev["platforms"]) != set(summary["platforms"]):
            warnings.append("Hai vòng có tập nền tảng khác nhau — chỉ so sánh phần chung. Phạm vi bằng chứng "
                            "không nên hẹp đi giữa các vòng.")
        cmp = compare(summary, prev)

    v, v_notes = verdict(summary, cmp, args.target)
    text = report(card, summary, cmp, v, v_notes, warnings, args.target, args.tablet_weight)
    print(text)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    if args.json_out:
        out = {
            "app": card.get("app"), "iteration": card.get("iteration"),
            "overall": round(summary["overall"], 1), "grade": summary["grade"], "verdict": v,
            "platforms": {p: {"raw": round(r["raw"], 1), "final": round(r["final"], 1), "grade": r["grade"],
                              "caps": [{"reason": why, "cap": c} for why, c in r["caps"]],
                              "dimensions": {d: x["effective"] for d, x in r["dims"].items()}}
                          for p, r in summary["results"].items()},
            "backlog": summary["backlog"],
            "delta": None if not cmp else {
                "overall": round(cmp["overall_delta"], 1),
                "platforms": {p: round(x, 1) for p, x in cmp["platform_delta"].items()},
                "regressions": [{"platform": p, "dimension": d, "delta": x} for p, d, x in cmp["regressions"]]},
        }
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
