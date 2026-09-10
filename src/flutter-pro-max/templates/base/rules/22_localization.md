---
description: Tiêu chuẩn Đa ngôn ngữ (Localization - l10n), Cấm Hardcode Chuỗi Text Giao diện
globs: lib/presentation/**/*.dart, lib/l10n/**/*
---

# Rule: Localization & Zero Hardcoded Strings

> Kích hoạt: Khi viết mã giao diện UI, hiển thị thông báo, dialog hoặc cấu hình ngôn ngữ

## 1. Nguyên Tắc Sống Còn: Không Hardcode Chuỗi Text (Zero Hardcoded Strings)

> 🔴 **CẤM:** Viết trực tiếp chuỗi văn bản cứng vào Widget UI, ví dụ: `Text('Đăng nhập')`, `Text('Welcome back')`, `SnackBar(content: Text('Có lỗi xảy ra'))`.  
> Mọi chuỗi hiển thị cho người dùng **BẮT BUỘC** phải được định nghĩa trong hệ thống đa ngôn ngữ (Localization).

---

## 2. Tiêu Chuẩn Triển Khai (l10n Standards)

| Tiêu chí | Quy định chuẩn |
| :--- | :--- |
| **Định dạng file** | Sử dụng file ARB (Application Resource Bundle): `app_en.arb`, `app_vi.arb`. |
| **Thư mục lưu trữ** | Đặt tại `lib/l10n/` hoặc theo kiến trúc feature module. |
| **Truy cập trong UI** | Sử dụng BuildContext extension: `context.l10n.loginButtonTitle`. |
| **Tham số động** | Định nghĩa placeholders trong file ARB, không dùng nối chuỗi (`+` hoặc `'$name'`). |

---

## 3. Bảng Đối Chiếu: Sai vs Đúng

| ❌ Vi phạm (Hardcoded string) | ✅ Đúng chuẩn (Localized) |
| :--- | :--- |
| `Text('Đăng nhập')` | `Text(context.l10n.signIn)` |
| `Text('Xin chào, ' + userName)` | `Text(context.l10n.greetingUser(userName))` |
| `Text('Bạn có $count thông báo')` | `Text(context.l10n.notificationCount(count))` (kèm plural logic) |
| `Text('Lưu thay đổi')` | `Text(context.l10n.saveChanges)` |

---

## 4. Mẫu Cấu Hình & Sử Dụng Chuẩn

### File ARB (`lib/l10n/app_en.arb`)

```json
{
  "@@locale": "en",
  "signIn": "Sign In",
  "@signIn": {
    "description": "Button label for user authentication"
  },
  "greetingUser": "Hello, {name}!",
  "@greetingUser": {
    "description": "Greeting shown on dashboard",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "Alex"
      }
    }
  }
}
```

### Tiện ích mở rộng truy cập nhanh (`context_extension.dart`)

```dart
// ✅ Giúp code UI ngắn gọn, dễ đọc
extension LocalizationContext on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this)!;
}
```

---

## 5. Quy Ước Đặt Tên Key: Tránh Báo Động Giả SAST (SAST False Positives Hardening)

Các công cụ phân tích bảo mật tĩnh (SAST, SonarQube, Code Sentinel, Trufflehog) thường quét regex tìm các biến hoặc key chứa từ khóa nhạy cảm.

### Quy ước tiền tố (Prefix Convention):
| Loại chuỗi UI | Tiền tố chuẩn | Ví dụ an toàn | ❌ Cấm đặt tên trơ trọi |
| :--- | :--- | :--- | :--- |
| Nhãn Form/Field | `lbl_` | `lbl_user_password`, `lbl_api_token` | `"password"`, `"token"` |
| Gợi ý Placeholder | `hint_` | `hint_enter_password`, `hint_search` | `"enter_secret"` |
| Tiêu đề màn hình | `title_` | `title_security_settings` | `"secret_key"` |
| Thông báo / Lỗi | `msg_` / `err_` | `msg_invalid_credentials`, `err_session_expired` | `"auth_failure"` |

> 🔴 **CẤM:** Đặt key như `"password": "Mật khẩu"`, `"api_key": "Mã định danh"`. Luôn dùng prefix (`lbl_password`) để SAST scanner hiểu đây là chuỗi hiển thị giao diện, không phải hardcoded credential.

---

## 6. Cấu Hình Allowlist / Exclude File Từ Điển Cho Máy Quét SAST

Khi chạy công cụ quét bảo mật tự động trên CI/CD, hãy cấu hình loại trừ (exclude) các file tài nguyên ngôn ngữ:

```properties
# Ví dụ sonar-project.properties / SAST exclude list
sonar.exclusions=lib/l10n/*.arb,assets/translations/**,lib/generated/intl/**,lib/generated/locale_keys.g.dart
```

---

> 💡 **Lợi ích:** Ứng dụng luôn sẵn sàng mở rộng ra thị trường quốc tế mà không phải tốn hàng tuần rà soát và bóc tách từng chuỗi text hardcode, đồng thời giữ báo cáo quét bảo mật sạch bóng lỗi giả.
