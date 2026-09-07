---
description: Quản lý State theo cấp độ (Native-First Escalation), ValueNotifier, ChangeNotifier
globs: lib/presentation/**/*.dart, lib/ui/**/*.dart
---

# Rule: State Management (Native-First)

> Kích hoạt: Khi quản lý trạng thái trong Widget, màn hình hoặc toàn bộ ứng dụng

## 1. Triết lý Cốt lõi: Native-First, Escalate khi Cần

> 🔴 **CẢNH BÁO VI PHẠM:** Tuyệt đối không tự ý thêm các thư viện quản lý state bên thứ ba (như Riverpod, Bloc, MobX, GetX) vào dự án nếu **người dùng chưa yêu cầu rõ ràng**.  
> Việc đưa thư viện ngoài vào để xử lý các bài toán state cục bộ đơn giản bị coi là **hành vi Over-engineering nghiêm trọng**.

---

## 2. Chính sách Quản lý State theo Kiến trúc

1. **Mặc định (Dự án mới / Module mới):** Tuân thủ Clean Architecture, state đặt tại Presentation layer (Notifier / ViewModel / Presentation Controller).
2. **Dự án bảo trì (Brownfield):** Giữ nguyên kiến trúc state hiện có của từng module (MVC Controller, MVVM ViewModel, Bloc, Provider...).
3. **Tính năng mới trong module cũ:** Ưu tiên đồng bộ với pattern state hiện hữu của module đó để giảm thiểu chi phí chuyển giao và bảo trì.

---

## 3. Thang Bậc Leo Thang (Escalation Hierarchy)

Ưu tiên giải pháp từ trên xuống dưới theo thứ tự:

| Cấp độ | Giải pháp kỹ thuật | Tình huống áp dụng |
| :---: | :--- | :--- |
| **Level 1** | `StatelessWidget` | Giao diện tĩnh hoàn toàn, không có trạng thái biến thiên. |
| **Level 2** | `ValueNotifier` + `ValueListenableBuilder` | Trạng thái nguyên tử đơn giản (Bật/tắt toggle, tăng giảm counter, cờ loading). |
| **Level 3** | `ChangeNotifier` + `ListenableBuilder` | Trạng thái phức tạp gồm nhiều trường dữ liệu (Form nhập liệu, giỏ hàng, bộ lọc). |
| **Level 4** | `InheritedWidget` / `Provider` | Trạng thái dùng chung (Shared state) giữa nhiều màn hình hoặc toàn ứng dụng. |
| **Level 5** | **Bloc / Riverpod** | **CHỈ KHI người dùng yêu cầu rõ ràng** hoặc dự án đã cài sẵn. |

---

## 4. Ánh xạ State Owner theo Kiến trúc

| Kiến trúc dự án | Vị trí nắm giữ State ưu tiên |
| :--- | :--- |
| **Clean Architecture** | Presentation Notifier / ViewModel |
| **MVC** | Controller |
| **MVVM** | ViewModel |
| **Legacy App (dùng setState)** | Tái cấu trúc thành Local State có phạm vi hẹp (Scoped Widget) |

---

## 5. Quy Tắc Bất Biến (Hard Constraints)

| ❌ Sai lầm phổ biến | ✅ Giải pháp chuẩn hóa |
| :--- | :--- |
| Cài Riverpod chỉ để quản lý 1 nút bấm | Dùng `ValueNotifier<bool>` tích hợp sẵn |
| Gọi `setState()` ở cấp Scaffold làm rebuild cả màn hình | Dùng `ValueListenableBuilder` bọc đúng vị trí Widget cần thay đổi |
| Đưa biến trạng thái cục bộ của 1 màn hình vào Global State | Khởi tạo State trong phạm vi nội bộ của màn hình đó |
| Thay đổi trực tiếp thuộc tính của object (Mutable mutation) | Trạng thái bất biến (Immutable) kết hợp phương thức `copyWith` |

---

## 6. Mẫu Triển Khai Chuẩn (Standard Patterns)

### Cấp độ 2: State đơn giản với `ValueNotifier`

```dart
// ✅ Gọn nhẹ, không rebuild toàn tree, không cần thư viện ngoài
class CounterView extends StatelessWidget {
  CounterView({super.key});

  final ValueNotifier<int> _counter = ValueNotifier<int>(0);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ValueListenableBuilder<int>(
          valueListenable: _counter,
          builder: (context, count, child) {
            return Text('Số lần bấm: $count', style: Theme.of(context).textTheme.headlineMedium);
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _counter.value++,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### Cấp độ 3: State phức tạp với `ChangeNotifier` & Immutability

```dart
// ✅ Quản lý form / nghiệp vụ màn hình mà không cần thư viện cồng kềnh
class CartNotifier extends ChangeNotifier {
  final List<CartItem> _items = [];
  List<CartItem> get items => List.unmodifiable(_items);

  void addItem(CartItem item) {
    _items.add(item);
    notifyListeners(); // Thông báo cập nhật UI
  }

  void removeItem(String id) {
    _items.removeWhere((element) => element.id == id);
    notifyListeners();
  }
}
```

> ⚠️ **TUYỆT ĐỐI KHÔNG:** Tự ý đổi framework state của dự án cũ trừ khi có yêu cầu bằng văn bản rõ ràng từ người dùng.