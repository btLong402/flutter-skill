---
name: mobile-tablet-ux-audit
description: Chấm điểm UI/UX app mobile + tablet (thang 0–100, 10 tiêu chí, có điểm riêng cho mobile và tablet) rồi tự cải thiện theo vòng lặp audit → sửa → chấm lại. Dùng skill này bất cứ khi nào người dùng muốn đánh giá, review, audit, chấm điểm, critique hoặc cải thiện giao diện / trải nghiệm app (iOS, Android, Flutter, React Native, SwiftUI, Jetpack Compose, Figma, screenshot), kiểm tra usability, accessibility, responsive/adaptive trên tablet, hoặc hỏi kiểu "UI này ổn chưa", "app này có đẹp/dễ dùng không", "làm sao cho tốt hơn" — kể cả khi họ chỉ gửi screenshot hoặc source code mà không nói chữ "audit". Use for UI/UX scoring, heuristic evaluation, design critique, tablet layout review and self-improving design loops.
---

# Mobile + Tablet UI/UX Audit & Self-Improve

Skill này biến việc "đánh giá UI/UX" từ cảm tính thành một quy trình lặp lại được: **thu bằng chứng → chấm theo rubric → xếp hạng lỗi → sửa → chấm lại → giữ hoặc hoàn tác**. Mục tiêu là để agent tự đo được app đang ở đâu, biết nên sửa gì trước, và biết chắc mỗi lần sửa có thực sự tốt lên hay không.

## Nguyên tắc cốt lõi (đọc kỹ — đây là thứ quyết định chất lượng)

1. **Không bằng chứng, không điểm cao.** Mỗi điểm phải kèm bằng chứng cụ thể (màn hình nào, element nào, số đo nào). Điểm ≥ 4 cần ≥ 2 bằng chứng. Cái gì chưa kiểm chứng được thì chấm 3 và ghi `confidence: low` — `score.py` sẽ tự chặn điểm của mục low-confidence ở mức 3.5 để agent không "tự thưởng" cho thứ chưa nhìn thấy.
2. **Hiệu chỉnh khắt khe.** Một app thương mại trung bình nằm ở 3.0–3.5/5. 5/5 là hiếm: chỉ cho khi đã soi kỹ trên cả ma trận thiết bị mà không tìm ra lỗi. Điểm 5 ở khắp nơi nghĩa là agent chưa nhìn đủ kỹ.
3. **Chấm mobile và tablet riêng.** Phần lớn app "đẹp trên điện thoại" thì tablet chỉ là UI điện thoại bị kéo giãn. Hai điểm riêng giúp lộ ra điều đó.
4. **Chấm lại độc lập.** Khi chấm lại sau khi sửa, chấm từ đầu dựa trên bằng chứng mới — đừng mở scorecard cũ ra rồi "nhích thêm 0.5". Chỉ so sánh sau khi đã chấm xong.
5. **Mỗi vòng sửa ít thay đổi (3–5 việc).** Sửa quá nhiều một lúc thì không biết thay đổi nào có tác dụng, cũng không biết cái nào gây hồi quy.
6. **Số liệu thắng cảm giác.** Contrast, kích thước vùng chạm, font size, khoảng cách → đo bằng `scripts/contrast.py` hoặc đọc từ code, không ước lượng bằng mắt.

## Cấu trúc skill

```
mobile-tablet-ux-audit/
├── SKILL.md                         ← workflow (file này)
├── references/
│   ├── rubric.md                    ← 10 tiêu chí, trọng số, mốc điểm 1/3/5, checklist
│   ├── platform-checks.md           ← ma trận thiết bị + kiểm tra riêng mobile / tablet
│   ├── evidence-collection.md       ← cách thu bằng chứng (screenshot / code / emulator / Figma)
│   └── improvement-playbook.md      ← lỗi thường gặp → cách sửa cụ thể, quy tắc vòng lặp
├── scripts/
│   ├── score.py                     ← tính điểm, áp trần, xếp backlog, so sánh vòng trước
│   └── contrast.py                  ← đo contrast WCAG + gợi ý màu đạt chuẩn
├── assets/
│   ├── scorecard.template.json      ← mẫu scorecard rỗng
│   └── example-scorecard.json       ← ví dụ đã điền (xem định dạng)
└── evals/evals.json                 ← prompt để kiểm thử skill
```

## Quy trình

### Bước 0 — Xác định phạm vi

Trả lời nhanh 4 câu từ ngữ cảnh người dùng đưa (chỉ hỏi lại nếu thực sự không suy ra được, và hỏi tối đa một câu):

- **Nền tảng:** iOS, Android hay cross-platform? Nếu app chỉ có mobile, bỏ cột tablet (scorecard chỉ cần `"platforms": ["mobile"]`).
- **Chế độ bằng chứng:** có screenshot, source code, app đang chạy (emulator/thiết bị), Figma? Xem `references/evidence-collection.md` để biết mỗi chế độ kiểm tra được gì và độ tin cậy ra sao.
- **Luồng chính (3–5 flow):** ví dụ onboarding, tìm kiếm, thanh toán. Audit theo flow chứ không chỉ theo màn hình đơn lẻ, vì lỗi UX hay nằm ở chỗ chuyển giữa các màn hình.
- **Người dùng mục tiêu & ngôn ngữ:** nếu app có tiếng Việt, áp dụng thêm các kiểm tra về dấu và độ dài chuỗi trong `references/platform-checks.md`.

### Bước 1 — Thu thập bằng chứng

Đọc `references/evidence-collection.md`, rồi thu theo **ma trận thiết bị** trong `references/platform-checks.md` (tối thiểu: 1 phone nhỏ, 1 phone lớn, tablet dọc, tablet ngang). Với mỗi flow cần có đủ các trạng thái: bình thường, loading, trống, lỗi, và (nếu có thể) font scale lớn + dark mode.

Ghi lại một **danh sách bằng chứng** có ID (ví dụ `S-home-phone-390`, `C-HomeScreen.dart:84`) để scorecard trích dẫn.

Nếu thiếu bằng chứng cho một khu vực (ví dụ không có tablet), nói rõ trong báo cáo và chấm các mục đó `confidence: low` — đừng đoán.

### Bước 2 — Chấm điểm

Đọc `references/rubric.md`. Chấm **10 tiêu chí × từng nền tảng**, thang 0–5, bước 0.5. Với mỗi ô điểm ghi:

```json
{ "score": 3.5, "confidence": "high", "evidence": ["S-home-phone-390: CTA nổi bật", "C-theme.dart:12: dùng token spacing"] }
```

Đồng thời ghi **danh sách lỗi (`issues`)** với: `id`, `dimension`, `platform` (`mobile|tablet|both`), `severity` (`blocker|major|minor|polish`), `screen`, `description`, `fix` (đề xuất cụ thể), `effort` (1=nhanh, 3=lớn), `reach` (1=một màn hình, 2=một flow, 3=toàn app). Lỗi phải đủ cụ thể để người khác tìm và sửa được ("nút Mua ở Cart cao 36dp" chứ không phải "nút hơi nhỏ").

Bắt đầu từ `assets/scorecard.template.json`; xem `assets/example-scorecard.json` để thấy định dạng đã điền.

### Bước 3 — Tính điểm bằng script (không tự cộng bằng tay)

```bash
python scripts/score.py scorecard.json --out report.md --json-out summary.json
# vòng sau:
python scripts/score.py scorecard.v1.json --previous scorecard.v0.json --out report.v1.md
```

Script sẽ: kiểm tra tính hợp lệ, tính điểm có trọng số cho từng nền tảng, áp **trần điểm** khi có lỗi chặn (blocker → ≤ 59; tiêu chí ≤ 1.5 → ≤ 69; accessibility < 3 → ≤ 79), tính điểm tổng, xếp **backlog ưu tiên**, và (nếu có `--previous`) báo delta + cảnh báo hồi quy.

Cần đo contrast trước khi chấm tiêu chí màu:

```bash
python scripts/contrast.py "#8A8A8E" "#FFFFFF" --size 14
python scripts/contrast.py --pairs pairs.json      # kiểm hàng loạt, có gợi ý màu sửa
```

### Bước 4 — Cải thiện

Lấy **3–5 mục đầu backlog** (script đã xếp theo `mức nghiêm trọng × phạm vi ảnh hưởng × trọng số tiêu chí ÷ công sức`). Đọc `references/improvement-playbook.md` để chọn cách sửa phù hợp rồi áp dụng. Khi sửa:

- Ưu tiên sửa ở **tầng token/theme/component dùng chung** hơn là vá từng màn hình — một chỗ sửa nâng nhiều màn hình và tránh lệch nhất quán.
- Không đổi thứ ngoài backlog (không "tiện tay" redesign), không xóa tính năng để điểm đẹp lên.
- Ghi mỗi thay đổi vào **iteration log** (issue ID, file/màn hình, mô tả ngắn).

### Bước 5 — Chấm lại và quyết định

Thu lại bằng chứng **trên đúng các thiết bị/trạng thái đã dùng ở vòng trước**, chấm lại độc lập (nguyên tắc 4), chạy `score.py --previous`. Sau đó:

| Kết quả | Hành động |
|---|---|
| Tổng tăng và không tiêu chí nào giảm ≥ 1 | **Giữ.** Đánh dấu các issue đã sửa `"status": "fixed"`, thêm issue mới (nếu sửa phát sinh lỗi). |
| Tổng giảm, hoặc có tiêu chí giảm ≥ 1 | **Hoàn tác** thay đổi gây hồi quy (xác định bằng cách tách từng thay đổi), rồi chấm lại. |
| Tổng tăng < 2 điểm | Cảnh báo **plateau** — xem lại: có đang sửa đúng nút thắt (tiêu chí nặng nhất còn thấp) không? |

### Điều kiện dừng

Dừng khi **một** trong các điều kiện sau thỏa:

- **Đạt:** điểm tổng ≥ 85, mỗi nền tảng ≥ 85 (sau khi áp trần), không còn blocker, không tiêu chí nào < 3.5.
- **Plateau:** 2 vòng liên tiếp tăng < 2 điểm → báo người dùng rằng phần còn lại cần quyết định thiết kế hoặc nghiên cứu người dùng thật, không phải thêm một vòng audit.
- **Giới hạn:** tối đa 5 vòng mỗi lần chạy, hoặc hết ngân sách thời gian.

## Báo cáo cuối cho người dùng

Trả lời bằng ngôn ngữ người dùng đang dùng. Cấu trúc:

1. **Điểm tổng + điểm mobile / tablet + hạng** (và nêu rõ nếu đã bị áp trần, vì sao).
2. **Điểm theo tiêu chí** (bảng từ `report.md`), nêu 2–3 tiêu chí mạnh nhất và yếu nhất.
3. **Top lỗi** (5–8 lỗi từ backlog): mô tả, vị trí, cách sửa.
4. **Lịch sử cải thiện** (nếu đã chạy vòng lặp): điểm theo từng vòng, đã sửa gì, đã hoàn tác gì.
5. **Giới hạn của lần audit này**: thiếu bằng chứng gì, chỗ nào confidence thấp, cái gì chỉ test người dùng thật mới trả lời được.

Hãy trung thực về giới hạn: điểm số từ agent là **heuristic evaluation** (đánh giá chuyên gia dựa trên quy chuẩn), không thay thế usability test với người dùng thật. Nói điều này một lần, ngắn gọn, ở mục 5.

## Những lỗi agent hay mắc khi dùng skill này

- **Lạm phát điểm** sau khi tự sửa (chấm cao vì "mình vừa sửa xong"). Cách chặn: chấm lại độc lập + bắt buộc có bằng chứng mới.
- **Chấm tablet theo phone** (vì không có screenshot tablet). Hãy thu bằng chứng tablet thật hoặc đánh dấu low-confidence.
- **Chỉ nhìn trạng thái "happy path"**. Phần lớn điểm bị mất nằm ở loading/empty/error, font lớn, và bàn phím che input.
- **Sửa cho điểm chứ không sửa cho người dùng**: ví dụ tăng cỡ chữ lên mà làm vỡ layout, hoặc thêm `contentDescription` rỗng cho đủ checklist. Nếu một thay đổi làm điểm tiêu chí này tăng nhưng tiêu chí khác giảm, ưu tiên kết quả chung và hoàn tác phần gây hại.
