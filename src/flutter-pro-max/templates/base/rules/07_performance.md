# Rule: Performance

> Kích hoạt: Khi viết widget, xử lý danh sách, hoặc async operations

## Nguyên tắc: Performance là requirement, không phải nice-to-have

### Widget Performance

| ❌ Sai | ✅ Đúng | Impact |
|--------|---------|--------|
| `Container()` cho spacing | `const SizedBox(height: 16)` | Giảm rebuild |
| `ListView(children: [...])` | `ListView.builder(itemBuilder:)` | Lazy loading |
| Widget không có `const` | `const MyWidget()` | Prevent rebuild |
| Inline function trong `build()` | Extract method hoặc cached | Tránh tạo closure mỗi frame |
| Rebuild toàn tree | `ValueListenableBuilder` scoped | Chỉ rebuild phần thay đổi |

### Async & Computation

| Quy tắc | Lý do |
|----------|-------|
| KHÔNG gọi API/async trong `build()` | Block UI thread |
| Heavy JSON parsing → dùng `compute()` | Chạy trên isolate riêng |
| Image caching → dùng `CachedNetworkImage` | Tránh download lại |
| Debounce search input (300-500ms) | Giảm API calls |

### State Management Performance

```dart
// ❌ Toàn widget tree rebuild
setState(() => _counter++);

// ✅ Chỉ rebuild phần cần thiết
ValueListenableBuilder<int>(
  valueListenable: _counter,
  builder: (_, value, child) => Text('$value'),
  child: const ExpensiveWidget(), // Không bị rebuild
);
```

### Checklist trước ship

- [ ] Tất cả widget có `const` constructor nếu có thể
- [ ] ListView/GridView dùng `.builder` hoặc `.separated`
- [ ] Không có `print()` còn sót (dùng `developer.log`)
- [ ] Images có loading/error builders

> 🔴 **Nếu list > 20 items → BẮT BUỘC dùng `.builder`.** Không exceptions.