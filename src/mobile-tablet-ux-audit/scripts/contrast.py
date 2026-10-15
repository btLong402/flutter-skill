#!/usr/bin/env python3
"""Đo tỉ lệ tương phản WCAG 2.x và gợi ý màu đạt chuẩn.

Dùng:
  python contrast.py "#8A8A8E" "#FFFFFF" --size 14
  python contrast.py "#777" "#FFF" --size 20 --bold
  python contrast.py "#9AA0A6" "#FFFFFF" --kind ui          # icon/viền/focus ring
  python contrast.py --pairs pairs.json                      # nhiều cặp một lượt

pairs.json: [{"name": "caption", "fg": "#8A8A8E", "bg": "#FFFFFF",
              "size": 12, "bold": false, "kind": "text"}, ...]

Ngưỡng:
  text thường        >= 4.5
  text lớn           >= 3.0  (>= 24px, hoặc >= 18.66px đậm; dp/pt/px coi như tương đương)
  thành phần UI/icon >= 3.0  (WCAG 1.4.11)

Hỗ trợ hex #RGB, #RGBA, #RRGGBB, #RRGGBBAA. Nếu fg có alpha, nó được trộn lên bg.
Mã thoát: 0 nếu tất cả đạt, 1 nếu có cặp trượt, 2 nếu đầu vào sai.
"""
import argparse
import json
import sys


def parse_hex(value):
    s = value.strip().lstrip("#")
    if len(s) in (3, 4):
        s = "".join(ch * 2 for ch in s)
    if len(s) == 6:
        s += "FF"
    if len(s) != 8:
        raise ValueError(f"Mã màu không hợp lệ: {value!r}")
    try:
        r, g, b, a = (int(s[i:i + 2], 16) for i in (0, 2, 4, 6))
    except ValueError:
        raise ValueError(f"Mã màu không hợp lệ: {value!r}") from None
    return r, g, b, a / 255.0


def composite(fg, bg):
    """Trộn fg (có alpha) lên bg đặc."""
    a = fg[3]
    return tuple(round(fg[i] * a + bg[i] * (1 - a)) for i in range(3))


def channel(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(rgb1, rgb2):
    l1, l2 = luminance(rgb1), luminance(rgb2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def to_hex(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


def required(kind, size, bold):
    if kind == "ui":
        return 3.0, "thành phần UI"
    large = size >= 24 or (bold and size >= 18.66)
    return (3.0, "text lớn") if large else (4.5, "text thường")


def suggest(fg_rgb, bg_rgb, target):
    """Pha fg về phía đen/trắng (xa nền hơn) cho tới khi đạt target; trả về hex hoặc None."""
    toward = (0, 0, 0) if luminance(bg_rgb) > 0.5 else (255, 255, 255)
    for step in range(1, 101):
        t = step / 100.0
        cand = tuple(round(fg_rgb[i] * (1 - t) + toward[i] * t) for i in range(3))
        if ratio(cand, bg_rgb) >= target:
            return to_hex(cand)
    return None


def check(name, fg, bg, size, bold, kind):
    bg_c = parse_hex(bg)
    bg_rgb = bg_c[:3]
    fg_rgb = composite(parse_hex(fg), bg_rgb)
    r = ratio(fg_rgb, bg_rgb)
    need, label = required(kind, size, bold)
    ok = r >= need
    return {
        "name": name, "fg": to_hex(fg_rgb), "bg": to_hex(bg_rgb),
        "ratio": round(r, 2), "required": need, "type": label,
        "pass": ok, "suggest": None if ok else suggest(fg_rgb, bg_rgb, need),
    }


def show(res):
    mark = "PASS" if res["pass"] else "FAIL"
    line = (f"[{mark}] {res['name']}: {res['fg']} trên {res['bg']} = {res['ratio']}:1 "
            f"(cần ≥ {res['required']}:1, {res['type']})")
    if not res["pass"] and res["suggest"]:
        new = check("", res["suggest"], res["bg"], 0, False, "ui")["ratio"]
        line += f"  → gợi ý fg: {res['suggest']} ({new}:1)"
    print(line)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fg", nargs="?", help="màu chữ/icon (hex)")
    ap.add_argument("bg", nargs="?", help="màu nền (hex)")
    ap.add_argument("--size", type=float, default=16, help="cỡ chữ (px/dp/pt), mặc định 16")
    ap.add_argument("--bold", action="store_true", help="chữ đậm")
    ap.add_argument("--kind", choices=["text", "ui"], default="text")
    ap.add_argument("--pairs", help="file JSON chứa nhiều cặp")
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    args = ap.parse_args()

    results = []
    try:
        if args.pairs:
            with open(args.pairs, encoding="utf-8") as f:
                for i, p in enumerate(json.load(f)):
                    results.append(check(p.get("name", f"pair-{i + 1}"), p["fg"], p["bg"],
                                         float(p.get("size", 16)), bool(p.get("bold", False)),
                                         p.get("kind", "text")))
        elif args.fg and args.bg:
            results.append(check("cặp màu", args.fg, args.bg, args.size, args.bold, args.kind))
        else:
            ap.error("cần <fg> <bg> hoặc --pairs file.json")
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            show(r)
        fails = sum(1 for r in results if not r["pass"])
        if len(results) > 1:
            print(f"\nTổng: {len(results) - fails}/{len(results)} đạt")
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
