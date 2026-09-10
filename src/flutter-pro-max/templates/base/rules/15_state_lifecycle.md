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

Mọi tài nguyên có trạng thái mở **BẮT BUỘC** phải được giải phóng đúng nơi:

| Loại tài nguyên | Phương thức giải phóng bắt buộc | Hậu quả nếu quên |
| :--- | :--- | :--- |
| `AnimationController` | `controller.dispose()` | CPU tiếp tục vẽ tick gây ngốn pin |
| `ScrollController` | `scrollController.dispose()` | Giữ tham chiếu Context, leak RAM |
| `TextEditingController` | `textController.dispose()` | Giữ listeners, leak bộ nhớ |
| `FocusNode` | `focusNode.dispose()` | Rò rỉ focus tree |
| `StreamSubscription` | `subscription.cancel()` | Tiếp tục nhận event ngầm, crash app |
| `Timer` | `timer.cancel()` | Tiếp tục chạy tick vô tận dưới nền |
| GetX `Worker` (`debounce`, `ever`) | `worker.dispose()` | Giữ lắng nghe stream Rx vĩnh viễn |

---

## 4. Rào Chắn Async Gap & Kiểm Soát Mounted (Mounted & Closed Guard)

Khi thực thi bất kỳ tác vụ bất đồng bộ (`await`) nào, cây Widget hoặc Controller có thể đã bị hủy trước khi dữ liệu phản hồi trả về.

### Trong `StatefulWidget`:
```dart
// 🔴 CẤM: Gọi setState() hoặc dùng context sau await mà không kiểm tra mounted
// ✅ ĐÚNG: Luôn đặt rào chắn mounted ngay sau mỗi await
Future<void> _handleRefresh() async {
  final data = await apiService.getData();
  if (!mounted) return; // BẮT BUỘC
  setState(() {
    _data = data;
  });
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Đã cập nhật')));
}
```

### Trong Controller (`GetxController`, `Bloc`, `ChangeNotifier`):
```dart
// ✅ GetX Controller: Kiểm tra isClosed trước khi update()
Future<void> fetchData() async {
  final res = await repository.fetch();
  if (isClosed) return; // BẮT BUỘC: Controller có thể đã bị remove khỏi memory
  data.value = res;
  update();
}

// ✅ Bloc / Cubit: Luôn kiểm tra !isClosed trước khi emit()
Future<void> onFetch(FetchEvent event, Emitter<State> emit) async {
  final res = await repository.fetch();
  if (!isClosed) {
    emit(State.loaded(res));
  }
}
```

---

## 5. Chuẩn Hóa Lifecycle Theo Framework (Framework Lifecycle Standards)

### 1. GetX Framework:
- **BẮT BUỘC:** Giải phóng tài nguyên trong `@override void onClose()`.
- **CẤM:** Tự viết hàm `void dispose()` trong `GetxController` vì GetX runtime chỉ tự động kích hoạt `onClose()`.
- **Dọn dẹp Worker:** Mọi `Worker` (`ever`, `interval`, `debounce`) và `StreamSubscription` phải được gán biến và hủy trong `onClose()`:
  ```dart
  class SearchController extends GetxController {
    late final Worker _searchWorker;
    StreamSubscription? _socketSub;

    @override
    void onInit() {
      super.onInit();
      _searchWorker = debounce(searchQuery, _performSearch, time: const Duration(milliseconds: 400));
    }

    @override
    void onClose() {
      _searchWorker.dispose();
      _socketSub?.cancel();
      super.onClose();
    }
  }
  ```

### 2. Provider / ChangeNotifier:
- Luôn gọi `super.dispose()` ở dòng cuối cùng của hàm `dispose()`.
- Đặt cờ `_disposed = true` nếu có tác vụ async lỡ dở, tránh gọi `notifyListeners()` sau khi đã giải phóng.

---

## 6. Cấm Tuyệt Đối Side-effects Trong Hàm `build()`

Hàm `build()` có thể bị gọi hàng chục lần mỗi giây trong quá trình render và animation:

| ❌ CẤM trong hàm `build()` | ✅ Giải pháp chuẩn |
| :--- | :--- |
| `Get.put(MyController())` hoặc `Get.find()` khởi tạo mới | Khởi tạo trong `Binding`, `initState()`, hoặc dùng `GetView<T>` |
| `TextEditingController()`, `ScrollController()` | Khởi tạo trong `initState()` và giải phóng trong `dispose()` |
| Gọi API hoặc Trigger async task (`fetchData()`) | Gọi trong `initState()`, Controller `onInit()`, hoặc qua event người dùng |
| Gọi `setState()` hoặc `controller.update()` | Chỉ gọi trong callbacks (`onPressed`, `onChanged`) hoặc sau khi render |

---

## 7. Ánh Xạ Trách Nhiệm theo Kiến Trúc

- **Clean Architecture:** Tầng Presentation (Widget / Notifier) chịu trách nhiệm giải phóng Controllers và UI Subscriptions; Tầng Data chịu trách nhiệm đóng kết nối DB / Client socket.
- **MVC:** Controller nắm giữ và chịu trách nhiệm `dispose()`/`onClose()` tất cả Streams, Timers và Subscriptions khi View bị hủy.
- **MVVM:** ViewModel chịu trách nhiệm dọn dẹp các luồng reactive (`dispose()`) khi người dùng rời khỏi màn hình.
