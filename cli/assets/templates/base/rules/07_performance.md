---
description: Tối ưu hiệu năng, const, ListView.builder, Async computation
globs: lib/presentation/**/*.dart, lib/ui/**/*.dart, lib/widgets/**/*.dart
---

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

### 4. Performance (Bài toán Scale)

Code chạy mượt ở 10 items có thể crash app ở 10,000 items. Lỗi tràn RAM (OOM - Out of Memory) thường âm thầm và khó debug.

| Quy mô | Giải pháp Render |
|--------|------------------|
| Ít items (< 20) | `Column` bọc trong `SingleChildScrollView` (Có thể chấp nhận) |
| Nhiều items (Hàng ngàn) | **BẮT BUỘC** dùng `ListView.builder` kết hợp Pagination/Infinite Scroll |
| Bảng dữ liệu lớn | PaginatedDataTable hoặc Virtualized Lists |

### Checklist trước ship

- [ ] Tất cả widget có `const` constructor nếu có thể
- [ ] ListView/GridView dùng `.builder` hoặc `.separated`
- [ ] Màn hình danh sách có hỗ trợ phân trang (Pagination) nếu data có thể phình to
- [ ] Không có `print()` còn sót (dùng `developer.log`)

> 🔴 **Nếu list > 20 items → BẮT BUỘC dùng `.builder`.** Luôn tự hỏi: *"Nếu user có 1 triệu record thì sao?"*