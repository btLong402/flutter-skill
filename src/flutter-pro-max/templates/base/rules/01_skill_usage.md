---
description: Tự động sử dụng Skill Search trước khi viết mã nguồn Flutter
globs: *
---

# Rule: Tự động sử dụng Skill

> Kích hoạt: Khi làm việc với các tệp tin Flutter/Dart hoặc chuẩn bị kiến trúc

**TRƯỚC KHI viết bất kỳ đoạn code Flutter nào**, bạn **BẮT BUỘC** phải tự động sử dụng skill để tra cứu kiến thức và mẫu thiết kế phù hợp. Tuyệt đối không được bỏ qua bước này.

---

## 1. Bảng Tra Cứu Domain theo Tình Huống

| Tình huống kỹ thuật | Domains cần tra cứu (`search.py`) |
| :--- | :--- |
| **Tạo UI / Màn hình mới** | `style`, `pattern`, `color`, `typography`, `landing` |
| **Chọn package / Thư viện** | `package` (kèm cờ lọc `--stack` nếu có) |
| **Thiết kế kiến trúc** | `architect`, `pattern` |
| **Tối ưu hiệu năng** | `performance` |
| **Khả năng tiếp cận** | `accessibility` |
| **Chưa rõ phong cách UI** | Dùng `--design-system` để sinh design system chuẩn |

---

## 2. Quy Trình Bắt Buộc (Workflow)

```
Yêu cầu người dùng 
    │
    ▼
Xác định Task Type (Greenfield / Brownfield) theo Architecture Decision Matrix (Rule 19)
    │
    ▼
Khai báo Pre-Flight Compliance Block (Rule 02)
    │
    ▼
Tra cứu Skill (search.py với ≥ 2 domains)
    │
    ▼
Đọc và phân tích kết quả tra cứu
    │
    ▼
Triển khai vào mã nguồn Dart thực tế
```

> 📖 **Tham chiếu:** [`19_architecture_decision_matrix.md`](file:///Users/longbt/Documents/dev/private/flutter-skill/src/flutter-pro-max/templates/base/rules/19_architecture_decision_matrix.md) để xác định đúng chiến lược kiến trúc và phạm vi tái cấu trúc trước khi sinh mã.

> 🔴 **CẢNH BÁO:** Viết code Flutter mà không tham khảo tri thức từ skill trước = Thiếu context chuẩn = Sinh mã chất lượng thấp và lỗi thời.