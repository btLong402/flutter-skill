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

### Data Protection

| Tình huống | Xử lý |
|------------|-------|
| User input | Sanitize trước khi gửi API |
| Hiển thị PII (email, phone) | Mask một phần: `john***@gmail.com` |
| Cache sensitive data | Encrypt hoặc không cache |
| Screenshot prevention | `FLAG_SECURE` cho screens nhạy cảm |

### Network Security

- HTTPS only (không HTTP)
- Certificate pinning cho apps quan trọng
- Timeout cho mọi API call (30s max)
- Không trust user input từ deep links

> 🔴 **Mỗi lần thêm API key hay xử lý auth**, kiểm tra checklist trên.