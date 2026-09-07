---
description: Xử lý Lỗi Mạng, Tránh Bão Request, Exponential Backoff, Circuit Breaker
globs: lib/data/**/*.dart, lib/services/**/*.dart, lib/repositories/**/*.dart, lib/core/network/**/*.dart
---

# Rule: Network & API Resiliency

> Kích hoạt: Khi viết API calls, cấu hình HTTP client (Dio / Http), xử lý timeout hoặc retry

## 1. Nguyên Tắc Cốt Lõi: Tránh Bão Request (Prevent Request Storms)

Khi server gặp sự cố hoặc quá tải (lỗi 500, 502, 503, 504 hoặc Timeout), **TUYỆT ĐỐI KHÔNG** dùng vòng lặp retry dồn dập (brute-force retry). Hành động này tạo ra bão request (thundering herd problem), khiến server đang quá tải sụp đổ hoàn toàn.

---

## 2. Các Kỹ Thuật Bắt Buộc

| Tình huống mạng | Kỹ thuật áp dụng | Mô tả triển khai |
| :--- | :--- | :--- |
| **Lỗi 5xx / Network Timeout** | **Exponential Backoff + Jitter** | Tăng lũy tiến thời gian chờ giữa các lần thử ($1\text{s} \rightarrow 2\text{s} \rightarrow 4\text{s} \rightarrow 8\text{s}$) kèm độ trễ ngẫu nhiên (Jitter) tránh dồn đồng loạt. |
| **Server sập liên tục (Down)** | **Circuit Breaker** | Tự động ngắt kết nối sau $N$ lần thất bại liên tiếp; từ chối gọi tiếp trong $T$ giây để server phục hồi. |
| **Mất kết nối hoàn toàn** | **Graceful UI Feedback** | Báo trạng thái thanh lịch (Snackbar/Banner), không quăng Exception làm crash đỏ màn hình. |

---

## 3. Mẫu Triển Khai Chuẩn: Dio Retry Interceptor

```dart
import 'dart:math';
import 'package:dio/dio.dart';

/// Interceptor xử lý Retry với Exponential Backoff và Jitter
class ResilientRetryInterceptor extends Interceptor {
  ResilientRetryInterceptor({
    required this.dio,
    this.maxRetries = 3,
    this.initialDelayMs = 1000,
  });

  final Dio dio;
  final int maxRetries;
  final int initialDelayMs;

  @override
  Future<void> onError(DioException err, ErrorInterceptorHandler handler) async {
    final requestOptions = err.requestOptions;
    final retryCount = (requestOptions.extra['retry_count'] as int?) ?? 0;

    // Chỉ retry với Network Timeout hoặc lỗi 5xx từ máy chủ
    final isServerError = err.response?.statusCode != null &&
        err.response!.statusCode! >= 500 &&
        err.response!.statusCode! <= 599;
    final isTimeout = err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout;

    if ((isServerError || isTimeout) && retryCount < maxRetries) {
      requestOptions.extra['retry_count'] = retryCount + 1;

      // Tính delay lũy tiến: base * 2^retry + jitter ngẫu nhiên
      final delayMs = (initialDelayMs * pow(2, retryCount)).toInt() +
          Random().nextInt(300);
      await Future<void>.delayed(Duration(milliseconds: delayMs));

      try {
        final response = await dio.fetch(requestOptions);
        return handler.resolve(response);
      } catch (e) {
        return super.onError(err, handler);
      }
    }

    return super.onError(err, handler);
  }
}
```

---

## 4. Ranh Giới Kiểm Tra (Self-Audit Question)

> 🔴 **Luôn tự vấn trước khi hoàn thành:**  
> *"Nếu API endpoint này trả về 503 hoặc đứt mạng giữa chừng, ứng dụng có bị treo đơ, văng màn hình đỏ hoặc spam request liên tục hay không?"*
