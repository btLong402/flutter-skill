---
description: Tự động sử dụng skill search trước khi viết code Flutter
globs: *
---

# Rule: Tự động sử dụng Skill

> Kích hoạt: Khi làm việc với Flutter/Dart files

**TRƯỚC KHI viết code Flutter**, bạn PHẢI tự động sử dụng skill để lấy knowledge phù hợp. Không được bỏ qua bước này.

| Tình huống | Domains cần search |
|------------|-------------------|
| Tạo UI/Screen mới | `style`, `pattern`, `color`, `typography`, `landing` |
| Chọn package/thư viện | `package` (kèm `--stack` filter nếu có) |
| Thiết kế kiến trúc | `architect`, `pattern` |
| Tối ưu performance | `performance` |
| Accessibility | `accessibility` |
| Không chắc UI style | Dùng `--design-system` để generate design system |

**Workflow bắt buộc:**

```
User request → Search skill (≥2 domains) → Đọc kết quả → Áp dụng vào code
```

> ⚠️ Viết code Flutter mà không tham khảo skill trước = thiếu context = code chất lượng thấp.