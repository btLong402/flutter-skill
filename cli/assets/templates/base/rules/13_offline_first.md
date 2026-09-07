---
description: Tư duy Offline-First, Cache dữ liệu Cục bộ, Luồng Stream Đồng bộ ngầm, Xử lý Mất mạng
globs: lib/data/**/*.dart, lib/repositories/**/*.dart, lib/presentation/**/*.dart
---

# Rule: Offline-First Experience

> Kích hoạt: Khi thiết kế tầng dữ liệu (Data layer), Repository hoặc fetch data cho các màn hình chính

## 1. Nguyên Tắc Cốt Lõi: Sống Sót Không Cần Mạng (Offline Resilience)

Khi thiết bị mất kết nối mạng hoặc ở vùng sóng yếu, **TUYỆT ĐỐI KHÔNG** để vòng xoay loading chạy vô tận hoặc văng ra màn hình trắng trơn. Người dùng vẫn phải xem được dữ liệu đã lưu gần nhất.

---

## 2. Kiến Trúc Luồng Dữ Liệu Offline-First

```
[UI Screen] ◄────── Stream / ValueNotifier ──────┐
     │                                            │
     ▼                                            │
[Repository] ── 1. Đọc ngay cache cũ ────────► [Local DB (Hive/Isar/SQLite)]
     │                                            ▲
     └── 2. Gọi ngầm Server (Remote) ─┐           │
                                      ▼           │
                                [API Service]     │
                                      │           │
                                      └── 3. Ghi dữ liệu mới vào ┘
```

1. **Hiển thị tức thì (Cache-First Render):** Nạp dữ liệu từ Local DB và đẩy lên UI ngay trong $\le 50\text{ms}$.
2. **Đồng bộ ngầm (Background Sync):** Kích hoạt gọi API ngầm lên server.
3. **Cập nhật mượt mà (Reactive Stream Update):** Khi có dữ liệu mới từ server, lưu vào Local DB; luồng Stream sẽ tự động phát tín hiệu cập nhật UI mà không làm giật lag giao diện.

---

## 3. Mẫu Triển Khai Chuẩn: Reactive Offline-First Repository

```dart
abstract class ProductRepository {
  /// Luồng dữ liệu phản ứng: Phát cache trước, cập nhật sau
  Stream<List<Product>> watchProducts();
}

class ProductRepositoryImpl implements ProductRepository {
  ProductRepositoryImpl({
    required this.localDataSource,
    required this.remoteDataSource,
  });

  final ProductLocalDataSource localDataSource;
  final ProductRemoteDataSource remoteDataSource;

  @override
  Stream<List<Product>> watchProducts() async* {
    // 1. Phát dữ liệu đã lưu trong Local DB ngay lập tức
    final cached = await localDataSource.getCachedProducts();
    if (cached.isNotEmpty) {
      yield cached;
    }

    // 2. Thử gọi API ngầm để cập nhật dữ liệu mới nhất
    try {
      final fresh = await remoteDataSource.fetchProducts();
      await localDataSource.saveProducts(fresh);
      yield fresh; // 3. Phát dữ liệu mới nếu thành công
    } catch (_) {
      // Khi mất mạng: Giữ nguyên dữ liệu cache, không quăng lỗi làm sập UI
      if (cached.isEmpty) rethrow; // Chỉ ném lỗi nếu không có cả cache
    }
  }
}
```

---

## 4. Checklist Thẩm Định Tính Năng Offline

- [ ] Khi ngắt kết nối Wi-Fi / 4G và mở lại ứng dụng, màn hình vẫn hiển thị dữ liệu cũ thay vì màn hình trống.
- [ ] Các thao tác ghi dữ liệu (Tạo mới, Sửa, Xóa) được đưa vào hàng đợi (`PendingActionQueue`) để tự động đồng bộ lại khi có mạng trở lại.
- [ ] Có thanh thông báo tinh tế (Offline Banner / Pill) thông báo cho người dùng biết ứng dụng đang chạy ở chế độ ngoại tuyến.
