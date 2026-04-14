---
description: Quản lý state theo cấp độ (Native-first), ValueNotifier
globs: lib/presentation/**/*.dart, lib/ui/**/*.dart
---

# Rule: State Management

> Kích hoạt: Khi quản lý state trong widget, screen, hoặc app-level

## Nguyên tắc: Native-First, Escalate khi cần

## Architecture-Aware Policy

1. **Mac dinh (code moi):** Follow Clean Architecture, state dat o presentation layer (notifier/view model/controller presentation).
2. **Maintenance du an cu:** Giu nguyen state stack hien co cua module (MVC Controller, MVVM ViewModel, Bloc, Provider...), khong ep migrate neu khong co yeu cau ro rang.
3. **Feature moi trong module cu:** Uu tien giong pattern state cua module do de giam chi phi maintain.

### Hierarchy (Ưu tiên từ trên xuống)

| Level | Giải pháp | Khi nào dùng |
|-------|-----------|-------------|
| 1️⃣ | `StatelessWidget` | UI tĩnh, không có state |
| 2️⃣ | `ValueNotifier` + `ValueListenableBuilder` | State đơn giản (counter, toggle, loading) |
| 3️⃣ | `ChangeNotifier` + `ListenableBuilder` | State phức tạp có nhiều fields (form, cart) |
| 4️⃣ | `InheritedWidget` / `Provider` | Shared state giữa nhiều widgets |
| 5️⃣ | Riverpod / Bloc | **CHỈ KHI user yêu cầu rõ ràng** |

### Mapping theo kien truc

| Kien truc | State owner uu tien |
|----------|-----------------------|
| Clean Architecture | Presentation Notifier / ViewModel |
| MVC | Controller |
| MVVM | ViewModel |
| Legacy setState app | Local state scoped widget/screen |

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

> ⚠️ **Khong tu y thay state framework cua du an cu.** Chi escalate (Riverpod/Bloc/GetX hoac migrate) khi user yeu cau ro rang.