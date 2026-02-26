---
description: Xử lý Vòng đời thiêt bị (Lifecycle), Orientation Change, Background State
globs: lib/presentation/**/*.dart, lib/logic/**/*.dart, lib/providers/**/*.dart
---

# Rule: State & Lifecycle Resilience

> Kích hoạt: Khi quản lý State (Bloc/Provider/Riverpod), xử lý orientation, handle app background state

## Nguyên tắc: Chống hao pin & lag vô ích

Quản lý vòng đời (lifecycle) kém sẽ làm máy nóng, lag và hao pin nhanh chóng, đặc biệt trên thiết bị Android yếu.

### Xử lý Lifecycle Events

1. **Xoay màn hình (Orientation Change):** 
   - Việc xoay dọc/ngang không được làm trigger lại các API requests. 
   - State phải được giữ nguyên bằng cơ chế State Management chuyên biệt, widget chỉ rebuild UI Layout.

2. **App chuyển vào nền (Backgrounded):**
   - Lập tức ngắt (Pause/Cancel) các Streams liên tục (như vị trí GPS, socket).
   - Tạm dừng các `Timer` đếm ngược.

3. **Memory Warning (Cảnh báo RAM):**
   - Clear cache hình ảnh trong bộ nhớ (ví dụ: xoá cache network images).
   - Giải phóng tài nguyên memory lớn không dùng tới.

### Rò rỉ bộ nhớ (Memory Leaks)
- Luôn gọi `dispose()` trên các Controller (AnimationController, ScrollController, TextEditingController).
- Đảm bảo huỷ (cancel) StreamSubscription khi Widget bị huỷ.
