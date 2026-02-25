# Rule: State Management

> Kích hoạt: Khi quản lý state trong widget, screen, hoặc app-level

## Nguyên tắc: Native-First, Escalate khi cần

### Hierarchy (Ưu tiên từ trên xuống)

| Level | Giải pháp | Khi nào dùng |
|-------|-----------|-------------|
| 1️⃣ | `StatelessWidget` | UI tĩnh, không có state |
| 2️⃣ | `ValueNotifier` + `ValueListenableBuilder` | State đơn giản (counter, toggle, loading) |
| 3️⃣ | `ChangeNotifier` + `ListenableBuilder` | State phức tạp có nhiều fields (form, cart) |
| 4️⃣ | `InheritedWidget` / `Provider` | Shared state giữa nhiều widgets |
| 5️⃣ | Riverpod / Bloc | **CHỈ KHI user yêu cầu rõ ràng** |

### Quy tắc cứng

| ❌ Sai | ✅ Đúng |
|--------|---------|
| Dùng Riverpod cho counter đơn giản | `ValueNotifier<int>` |
| `setState` rebuild toàn screen | `ValueListenableBuilder` scoped |
| Global state cho state chỉ 1 screen dùng | Local state trong widget |
| Mutable state trực tiếp | Immutable state + `copyWith` |

### Pattern chuẩn

```dart
// ✅ Simple: ValueNotifier
class CounterWidget extends StatelessWidget {
  final _count = ValueNotifier<int>(0);

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<int>(
      valueListenable: _count,
      builder: (_, value, __) => Text('$value'),
    );
  }
}

// ✅ Complex: ChangeNotifier
class CartNotifier extends ChangeNotifier {
  final List<Item> _items = [];
  List<Item> get items => List.unmodifiable(_items);

  void add(Item item) {
    _items.add(item);
    notifyListeners();
  }
}
```

> ⚠️ **KHÔNG tự ý thêm Riverpod/Bloc/GetX.** Hỏi user trước nếu cần escalate.
