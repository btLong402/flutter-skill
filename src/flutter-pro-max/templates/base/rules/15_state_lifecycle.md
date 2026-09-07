---
description: Quản lý Vòng đời Thiết bị (Lifecycle), Xoay màn hình, App Background State, Giải phóng Bộ nhớ
globs: lib/**/*.dart
---

# Rule: State & Lifecycle Resilience

> Kích hoạt: Khi quản lý state (Clean / MVC / MVVM / Provider / Bloc), xử lý xoay màn hình hoặc background state

## 1. Nguyên Tắc Cốt Lõi: Chống Hao Pin, Nóng Máy & Lag

Việc quản lý vòng đời ứng dụng cẩu thả sẽ gây rò rỉ bộ nhớ (Memory Leak), làm nóng máy và tiêu hao pin nghiêm trọng, đặc biệt trên các dòng điện thoại Android cấu hình yếu.

---

## 2. Xử Lý Các Sự Kiện Vòng Đời (Lifecycle Events)

### 1. Xoay màn hình (Orientation Change)
- Xoay dọc/ngang chỉ được phép rebuild lại bố cục giao diện (Layout).
- **TUYỆT ĐỐI KHÔNG** để việc xoay màn hình kích hoạt lại các yêu cầu gọi API hoặc khởi tạo lại State từ đầu.
- Nắm giữ State ở Controller / Notifier nằm ngoài lifecycle của Widget dựng hình.

### 2. Ứng dụng chuyển vào chạy ngầm (Backgrounded / Paused)
- Lập tức tạm dừng (Pause) hoặc hủy (Cancel) các luồng dữ liệu liên tục: Định vị GPS, Camera feed, WebSocket, Sensor.
- Hủy hoặc tạm dừng các `Timer` chu kỳ (`Timer.periodic`).

### 3. Cảnh báo đầy bộ nhớ (Memory Pressure)
- Xóa bộ nhớ đệm hình ảnh tạm thời (`imageCache.clear()`).
- Hủy các danh sách dữ liệu kích thước lớn không nằm trong màn hình hiện tại.

---

## 3. Checklist Bắt Buộc: Chống Rò Rỉ Bộ Nhớ (Memory Leaks)

Mọi tài nguyên có trạng thái mở **BẮT BUỘC** phải được giải phóng trong phương thức `dispose()`:

| Loại tài nguyên | Phương thức giải phóng bắt buộc | Hậu quả nếu quên |
| :--- | :--- | :--- |
| `AnimationController` | `controller.dispose()` | CPU tiếp tục vẽ tick gây ngốn pin |
| `ScrollController` | `scrollController.dispose()` | Giữ tham chiếu Context, leak RAM |
| `TextEditingController` | `textController.dispose()` | Giữ listeners, leak bộ nhớ |
| `FocusNode` | `focusNode.dispose()` | Rò rỉ focus tree |
| `StreamSubscription` | `subscription.cancel()` | Tiếp tục nhận event ngầm, crash app |
| `Timer` | `timer.cancel()` | Tiếp tục chạy tick vô tận dưới nền |

---

## 4. Ánh Xạ Trách Nhiệm theo Kiến Trúc

- **Clean Architecture:** Tầng Presentation (Widget / Notifier) chịu trách nhiệm giải phóng Controllers và UI Subscriptions; Tầng Data chịu trách nhiệm đóng kết nối DB / Client socket.
- **MVC:** Controller nắm giữ và chịu trách nhiệm `dispose()` tất cả Streams, Timers và Subscriptions khi View bị hủy.
- **MVVM:** ViewModel chịu trách nhiệm dọn dẹp các luồng reactive (`dispose()`) khi người dùng rời khỏi màn hình.
