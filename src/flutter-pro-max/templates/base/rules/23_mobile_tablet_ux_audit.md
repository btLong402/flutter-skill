---
description: Quy chuẩn đánh giá, audit và tự cải thiện chất lượng UI/UX đa nền tảng (Mobile & Tablet) định lượng bằng scorecard và công cụ đo
globs: *
---

# Rule: Đánh Giá & Tự Cải Thiện Chất Lượng UI/UX (Mobile & Tablet)

> Kích hoạt: Khi thiết kế, review, audit, refactor giao diện UI Flutter, kiểm tra độ tương phản, khả năng tiếp cận (Accessibility), hoặc điều chỉnh layout thích ứng Tablet & màn hình lớn.

Mọi đánh giá và cải thiện UI/UX phải là một quy trình kỹ thuật lặp lại được (**Evidence → Rubric Scoring → Prioritized Backlog → Fix → Re-audit**), tuyệt đối không nhận xét cảm tính hoặc ước lượng bằng mắt.

---

## 1. Nguyên Tắc Cốt Lõi (Core Principles)

1. **Không bằng chứng, không điểm cao:**
   - Mỗi đánh giá phải chỉ rõ màn hình (`screen`), phần tử (`element`) và số đo cụ thể (dp, contrast ratio, font size).
   - Điểm $\ge 4.0/5$ bắt buộc phải có $\ge 2$ bằng chứng thực chứng.
   - Chưa kiểm chứng được $\to$ chấm $3.0$ và gán `confidence: low` (công cụ `score.py` sẽ tự động chặn trần ở mức $3.5$).

2. **Chấm riêng Mobile và Tablet:**
   - Trải nghiệm Phone và Tablet hoàn toàn khác biệt. Tablet không được phép chỉ là UI điện thoại bị kéo giãn (stretched phone UI).
   - Khi chiều rộng $\ge 600\text{dp}$: Bắt buộc dùng `NavigationRail` thay cho `BottomNavigationBar`, áp dụng layout List-Detail hoặc multi-pane.

3. **Số liệu thắng cảm giác (Data > Intuition):**
   - Đo tỉ lệ tương phản WCAG bằng `scripts/contrast.py`.
   - Vùng chạm tối thiểu $48 \times 48\text{dp}$, khoảng cách giữa các interactive elements $\ge 8\text{dp}$.
   - Đo chiều dài dòng văn bản trên tablet: Không vượt quá $60–80$ ký tự / dòng để đảm bảo khả năng đọc.

4. **Vòng lặp tự cải thiện (Self-Improvement Loop):**
   - Mỗi vòng sửa chỉ tập trung **3–5 lỗi hàng đầu** trong Backlog ưu tiên. Sửa quá nhiều một lúc sẽ gây khó khăn trong việc kiểm soát hồi quy (regression).
   - Chấm lại độc lập: Sau khi sửa, ghi nhận bằng chứng mới và chấm lại từ đầu, không "tự cộng thêm điểm" dựa trên scorecard cũ.

---

## 2. Công Thức Ưu Tiên Backlog (Prioritization Formula)

Mỗi lỗi phát hiện được xếp hạng tự động trong `score.py` theo công thức:

$$\text{Priority} = \frac{\text{Severity} \times \text{Reach} \times \text{Dimension Weight}}{\text{Effort}}$$

Trong đó:
- **Severity (Mức độ nghiêm trọng):** `blocker: 8`, `major: 4`, `minor: 2`, `polish: 1`.
- **Reach (Phạm vi ảnh hưởng):** `3` (toàn app / luồng chính), `2` (nhiều màn hình), `1` (màn hình phụ / góc khuất).
- **Dimension Weight (Trọng số tiêu chí):** Từ $6$ đến $14$ điểm theo Rubric 10 tiêu chí.
- **Effort (Công sức sửa):** `1` (dễ, sửa token/styling), `2` (trung bình), `3` (khó, tái cấu trúc layout/state).

---

## 3. Các Trần Điểm Chặn (Hard Score Caps)

Dù tổng điểm thô cao, điểm cuối cùng của nền tảng sẽ bị chặn nếu vi phạm các ngưỡng tới hạn:
- **Blocker còn mở:** Điểm tối đa bị chặn ở **59/100** (Hạng Kém).
- **Có bất kỳ tiêu chí nào $\le 1.5/5$:** Điểm tối đa bị chặn ở **69/100** (Cần cải thiện).
- **Khả năng tiếp cận (Accessibility) $< 3.0/5$:** Điểm tối đa bị chặn ở **79/100** (Đạt).

---

## 4. Quy Trình Sử Dụng Công Cụ

### Bước 1: Kiểm tra tương phản màu (WCAG Contrast)
```bash
# Đo tương phản cặp màu đơn lẻ
python3 scripts/contrast.py "#8A8A8E" "#FFFFFF" --size 14

# Đo tương phản icon/viền UI
python3 scripts/contrast.py "#9AA0A6" "#FFFFFF" --kind ui

# Đo hàng loạt cặp màu từ file JSON
python3 scripts/contrast.py --pairs pairs.json --json
```

### Bước 2: Chấm điểm Scorecard
```bash
# Chấm điểm và in báo cáo Markdown
python3 scripts/score.py scorecard.json --out report.md --json-out summary.json

# So sánh với vòng trước để phát hiện hồi quy
python3 scripts/score.py scorecard.v1.json --previous scorecard.v0.json
```

### Bước 3: Đánh giá kết luận (Verdict)
- **PASS:** Điểm tổng và từng nền tảng $\ge 85.0$, không còn lỗi blocker, mọi tiêu chí $\ge 3.5$.
- **CONTINUE:** Chưa đạt mục tiêu $\to$ Lấy 3–5 lỗi đầu backlog để sửa tiếp.
- **REVERT_RECOMMENDED:** Điểm tổng giảm hoặc có tiêu chí giảm $\ge 1.0$ điểm $\to$ Ngay lập tức kiểm tra và hoàn tác thay đổi gây hồi quy.
- **PLATEAU_WARNING:** Điểm chỉ tăng $< 2.0$ điểm $\to$ Rà soát lại xem có đang giải quyết đúng nút thắt cổ chai hay không.

> 📖 **Tài liệu tham khảo chuyên sâu trong skill `mobile-tablet-ux-audit`:**
> - `references/rubric.md`: Chi tiết 10 tiêu chí, trọng số, mốc điểm 1/3/5 và checklist.
> - `references/platform-checks.md`: Checklist riêng cho Mobile (iOS, Android) và Tablet (iPadOS, Foldable).
> - `references/evidence-collection.md`: Hướng dẫn cách trích xuất bằng chứng từ code Dart và screenshots.
> - `references/improvement-playbook.md`: Cẩm nang sửa nhanh các lỗi thường gặp trong Flutter.
