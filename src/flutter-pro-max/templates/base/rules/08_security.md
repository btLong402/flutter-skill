---
description: Bảo mật, API Keys, Authentication, Data Protection
globs: lib/data/**/*.dart, lib/services/**/*.dart, lib/core/env/*.dart
---

# Rule: Security

> Kích hoạt: Khi xử lý authentication, API keys, user data, hoặc storage

## Nguyên tắc: Bảo mật không phải optional

### API Keys & Secrets

| ❌ KHÔNG BAO GIỜ | ✅ Thay bằng |
|-------------------|-------------|
| Hardcode API key trong source | Dùng `--dart-define` hoặc `.env` |
| Commit `.env` file | Thêm vào `.gitignore` |
| Log sensitive data | Mask/redact trước khi log |
| Lưu token trong `SharedPreferences` | Dùng `flutter_secure_storage` |

### Authentication

| Quy tắc | Chi tiết |
|----------|----------|
| Token storage | `flutter_secure_storage` (encrypted) |
| Token refresh | Interceptor tự động refresh khi 401 |
| Logout | Clear ALL tokens + secure storage |
| Deep link auth | Validate state parameter |

### Data Protection & File I/O Security

| Tình huống | Xử lý |
|------------|-------|
| User input | Sanitize trước khi gửi API |
| Hiển thị PII (email, phone) | Mask một phần: `john***@gmail.com` |
| Cache sensitive data | Encrypt hoặc không cache |
| Screenshot prevention | `FLAG_SECURE` cho screens nhạy cảm |
| Tải / Lưu file từ API | **Chống Path Traversal**: Dùng `path.basename()` + regex làm sạch, KHÔNG nối thẳng string đường dẫn |
| Upload File | Giới hạn dung lượng tối đa (vd: <= 10MB) và kiểm tra whitelist định dạng / MIME type |

#### Chống Path Traversal khi lưu file:
```dart
import 'package:path/path.dart' as p;

// ❌ CẤM: File('${dir.path}/$remoteFileName') -> Lỗ hổng ghi đè file hệ thống qua ../../
// ✅ ĐÚNG: Sanitize tên file trước khi tạo File object
String sanitizeFileName(String unsafeName) {
  final cleanName = p.basename(unsafeName).replaceAll(RegExp(r'[^\w\.-]'), '_');
  return cleanName.isEmpty ? 'downloaded_file' : cleanName;
}

final safePath = p.join(saveDir.path, sanitizeFileName(remoteFileName));
final file = File(safePath);
```

---

### Network & WebView Hardening

- HTTPS only (không dùng HTTP không mã hóa).
- Certificate pinning cho các ứng dụng ngân hàng / thanh toán / nhạy cảm.
- Timeout cho mọi API call (mặc định 30s max).
- Không trust user input từ deep links.

#### 1. WebView Security Guard:
```dart
// ❌ CẤM: Bỏ qua lỗi SSL (MITM vulnerability)
// onReceivedServerTrustAuthRequest: (controller, challenge) async {
//   return ServerTrustAuthResponse(action: ServerTrustAuthResponseAction.PROCEED); // LỖ HỔNG NGUY HIỂM!
// }

// ✅ ĐÚNG: Luôn từ chối hoặc chỉ cho phép domain tin cậy có chứng chỉ hợp lệ
InAppWebView(
  initialSettings: InAppWebViewSettings(
    allowUniversalAccessFromFileURLs: false,
    allowFileAccessFromFileURLs: false,
  ),
  shouldOverrideUrlLoading: (controller, navigationAction) async {
    final uri = navigationAction.request.url;
    // BẮT BUỘC: Khóa chỉ cho phép HTTPS và nằm trong domain allowlist
    if (uri != null && uri.scheme == 'https' && uri.host.endsWith('trusteddomain.com')) {
      return NavigationActionPolicy.ALLOW;
    }
    return NavigationActionPolicy.CANCEL;
  },
)
```

---

### Log Masking (Chống Rò Rỉ Token / Mật Khẩu Trong Log)

- **CẤM:** Ghi log chứa `password`, `token`, `refresh_token`, `accessToken`, `credit_card`.
- Bắt buộc cấu hình Interceptor của Dio / HTTP Client để tự động che thông tin:

```dart
class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    final headers = Map<String, dynamic>.from(options.headers);
    if (headers.containsKey('Authorization')) {
      headers['Authorization'] = 'Bearer ***MASKED***';
    }
    developer.log('--> ${options.method} ${options.uri}', name: 'HTTP');
    // KHÔNG log body nếu chứa thông tin đăng nhập nhạy cảm (password, pin, otp)
    if (!options.path.contains('/auth/login') && !options.path.contains('/otp')) {
      developer.log('Body: ${options.data}', name: 'HTTP');
    }
    handler.next(options);
  }
}
```

---

> 🔴 **Mỗi lần thêm API key, xử lý auth, tải file hoặc nhúng WebView**, kiểm tra checklist trên.