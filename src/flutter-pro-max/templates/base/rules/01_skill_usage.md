---
description: Tự động sử dụng Skill Search & UI/UX Audit theo ngữ cảnh nhiệm vụ (Context-Aware)
globs: *
---

# Rule: Tự Động Sử Dụng Skill Theo Ngữ Cảnh

> Kích hoạt: Khi làm việc với mã nguồn Flutter/Dart, thiết kế kiến trúc, hoặc review/audit giao diện UI/UX.

Tùy theo **bản chất nhiệm vụ (Task Type)**, bạn cần tự động kích hoạt skill và công cụ phù hợp nhằm cân bằng tối ưu giữa **chất lượng mã nguồn** và **tốc độ phản hồi**:

---

## 1. Phân Luồng Kích Hoạt (Routing Matrix)

### 🔴 Luồng BẮT BUỘC dùng Skill (Full Flight)
*Bắt buộc phải tra cứu skill trước khi sinh mã hoặc khi thực hiện kiểm định:*
- **Tạo UI / Màn hình mới (Greenfield):** Bắt buộc tra cứu `style`, `pattern`, `color`, `typography` hoặc dùng `--design-system` để sinh design system chuẩn.
- **Thiết kế kiến trúc / Chọn Package:** Tra cứu `architect`, `package` (kèm cờ lọc `--stack` nếu có).
- **Tối ưu hiệu năng & Bộ nhớ:** Tra cứu `performance`.
- **Audit / Review UI/UX & Responsive Tablet:** Bắt buộc kích hoạt skill `mobile-tablet-ux-audit` (`score.py`, `contrast.py`, rubric).
- **Tái cấu trúc lớn (Major Refactoring):** Tra cứu pattern kiến trúc để tránh logic leakage.

### ⚡ Luồng ĐI TẮT (Fast-Path — Không ép buộc tra cứu)
*Cho phép phân tích và sửa trực tiếp dựa trên ngữ cảnh file hiện hữu:*
- **Hotfix cục bộ (< 15 dòng):** Sửa lỗi null-safety, sửa chính tả/copy text, sửa logic if-else đơn giản đã rõ nguyên nhân.
- **Tái cấu trúc vi mô (Local Refactor):** Đổi tên biến, tách private helper widget trong cùng 1 file, format code.
- **Hỏi đáp & Giải thích code:** Khi người dùng chỉ yêu cầu giải thích luồng hoạt động mà không yêu cầu tìm kiếm giải pháp mới.

---

## 2. Bảng Tra Cứu Công Cụ & Domain theo Tình Huống

| Tình huống kỹ thuật | Công cụ / Domains cần tra cứu |
| :--- | :--- |
| **Tạo UI / Màn hình mới** | `search.py`: `style`, `pattern`, `color`, `typography`, `landing` |
| **Chọn package / Thư viện** | `search.py`: `package` (kèm cờ lọc `--stack` nếu có) |
| **Thiết kế kiến trúc** | `search.py`: `architect`, `pattern` |
| **Tối ưu hiệu năng** | `search.py`: `performance` |
| **Khả năng tiếp cận** | `search.py`: `accessibility` & skill `mobile-tablet-ux-audit` |
| **Chưa rõ phong cách UI** | `search.py`: `--design-system` để sinh design system chuẩn |
| **Kiểm tra tương phản màu** | Skill `mobile-tablet-ux-audit`: `python3 contrast.py <fg> <bg>` |
| **Audit & chấm điểm UI/UX** | Skill `mobile-tablet-ux-audit`: `python3 score.py scorecard.json` |
| **Review Tablet / Adaptive** | Skill `mobile-tablet-ux-audit`: Rubric 10 tiêu chí cho mobile + tablet |

---

## 3. Quy Trình Thực Hiện (Workflow)

```
Yêu cầu người dùng
    │
    ▼
Phân loại Task Type: Hotfix nhỏ / Fast-Path hay Tính năng mới / Kiến trúc / Audit?
    ├── [Fast-Path (<15 dòng, typo, bug cục bộ)] ──────────┐
    │                                                      │
    ▼ [Full Flight]                                        │
Xác định Task Type theo Architecture Decision Matrix (R19) │
    │                                                      │
    ▼                                                      │
Khai báo Pre-Flight Compliance Block (R02)                 │
    │                                                      │
    ▼                                                      │
Tra cứu Skill Code (search.py) & UI/UX Audit (R23)         │
    │                                                      │
    ▼                                                      │
Đọc & phân tích kết quả tra cứu                            │
    │                                                      │
    ▼                                                      │
Triển khai vào mã nguồn Dart thực tế ◄─────────────────────┘
    │
    ▼
Audit UI/UX định lượng (nếu có thay đổi UI) → Sửa backlog ưu tiên (Rule 23)
```

> 📖 **Tham chiếu:**
> - [`19_architecture_decision_matrix.md`](file:///Users/longbt/Documents/dev/private/flutter-skill/src/flutter-pro-max/templates/base/rules/19_architecture_decision_matrix.md) để xác định đúng chiến lược kiến trúc và phạm vi tái cấu trúc trước khi sinh mã.
> - [`23_mobile_tablet_ux_audit.md`](file:///Users/longbt/Documents/dev/private/flutter-skill/src/flutter-pro-max/templates/base/rules/23_mobile_tablet_ux_audit.md) để thực hiện quy trình audit và tự cải thiện UI/UX có căn cứ định lượng.

> 🔴 **CẢNH BÁO:** Bỏ qua tra cứu khi làm tính năng mới = Thiếu context chuẩn = Sinh mã chất lượng thấp. Chế tác UI mà không audit tương phản và tablet = UI vỡ trên thiết bị thực tế.