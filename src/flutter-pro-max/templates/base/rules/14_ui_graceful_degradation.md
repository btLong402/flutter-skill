---
description: Xử lý Graceful Degradation, Fallback UI khi component/dữ liệu lỗi
globs: lib/presentation/**/*.dart, lib/ui/**/*.dart, lib/widgets/**/*.dart
---

# Rule: Graceful Degradation (UI Fallback)

> Kích hoạt: Khi build UI components, handle Image Network, List Items

## Nguyên tắc: Lỗi cục bộ không được sập toàn cục

Khi một thành phần UI hoặc dữ liệu bị fail, **đừng làm sập cả màn hình**. Tính thanh lịch của app nằm ở việc fallback giấu lỗi.

### Các Fallback Pattern Bắt Buộc

| Lỗi Component | Giải pháp UI (Fallback) |
|---------------|-------------------------|
| Hình ảnh (Avatar, Banner) lỗi tải (CDN down/404) | Hiển thị Default Image Icon, Placeholder, hoặc Chữ cái đầu của Tên (Initials Avatar). |
| 1 Item lỗi trong ListView | Hiển thị `ErrorItemWidget` nhỏ cho riêng dòng đó, thay vì ném Exception break toàn list. |
| Font chữ không tải được | Cấu hình Fallback về System Font mặc định. |
| Widget tương tác lỗi | Vô hiệu hoá (Disable) nút bấm đó và đổi màu xám thay vì crash khi bấm. |

> 🔴 **Quy tắc vàng:** Luôn định nghĩa thuộc tính `errorBuilder` cho mọi Network Image.
