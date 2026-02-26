---
description: Xử lý Network Failures, Tránh bão Request, Exponential Backoff, Circuit Breaker
globs: lib/data/**/*.dart, lib/services/**/*.dart, lib/repositories/**/*.dart
---

# Rule: Network & API Resiliency

> Kích hoạt: Khi viết API calls, cấu hình HTTP clients (Dio/Http), xử lý timeout

## Nguyên tắc: Tránh bão Request

Khi API lỗi do server quá tải, **TUYỆT ĐỐI KHÔNG** dùng vòng lặp retry vô tội vạ, vì sẽ tạo thêm gánh nặng làm sập hẳn server đang "thở oxy".

### Giải pháp bắt buộc

| Tình huống | Kỹ thuật áp dụng |
|------------|------------------|
| Lỗi 5xx / Timeout | **Exponential Backoff**: Tăng thời gian chờ sau mỗi lần thử (vd: 1s, 2s, 4s, 8s...) |
| Server chết liên tục | **Circuit Breaker**: Ngắt hoàn toàn request trong 1 khoảng thời gian nhất định để server phục hồi. |
| Mạng chập chờn | Cảnh báo UI thanh lịch (Snackbar / Retry button), không quăng exception đỏ màn hình. |

> 🔴 **Luôn tự hỏi:** *"Nếu API endpoint này sập, app của mình có sập theo hay không bị treo cứng không?"*
