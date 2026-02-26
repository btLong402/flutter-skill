---
description: Tư duy Offline-First, Cache dữ liệu, Đồng bộ ngầm, Xử lý khi mất mạng
globs: lib/data/**/*.dart, lib/repositories/**/*.dart, lib/presentation/**/*.dart
---

# Rule: Offline-First Experience

> Kích hoạt: Khi thiết kế luồng dữ liệu, fetch data cho màn hình chính (Dashboard, List)

## Nguyên tắc: Sống sót không cần mạng

Khi thiết bị lọt vào vùng mất mạng, **TUYỆT ĐỐI KHÔNG** để vòng xoay loading chạy vô tận hoặc văng ra màn hình trắng trơn.

### Kiến trúc Offline-First

1. **Lớp Cache Cache:** Bắt buộc có Local DB (SQLite, Isar, Hive) để lưu dữ liệu quan trọng.
2. **Luồng ưu tiên Local:**
   - Khi mở màn hình: Load data từ Local DB hiển thị lên UI **ngay lập tức**.
   - Kích hoạt đồng bộ ngầm (background fetch) với server.
   - Khi có data mới từ server: Cập nhật DB nội bộ, luồng stream tự động đẩy data thiết kế mới lên UI một cách mượt mà.

### Checklist Offline
- [ ] Mở app khi ngắt Wi-Fi vẫn thấy được dữ liệu cũ.
- [ ] Thao tác (Like, Xoá, Nút bấm) được lưu tạm hàng đợi (Queue) để sync lại khi có mạng.
- [ ] Có thông báo tinh tế báo hiệu đang xài ở chế độ Offline.
