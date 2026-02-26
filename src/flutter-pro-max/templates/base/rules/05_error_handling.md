---
description: Xử lý lỗi, Try-catch, Result pattern, Không fail im lặng
globs: lib/data/**/*.dart, lib/services/**/*.dart, lib/repositories/**/*.dart, lib/domain/**/*.dart
---

# Rule: Error Handling

> Kích hoạt: Khi viết logic xử lý dữ liệu, API calls, hoặc async operations

## Nguyên tắc: Không bao giờ fail im lặng

### Bắt buộc

| Tình huống | Cách xử lý |
|------------|------------|
| API call | Luôn wrap trong `try-catch`, log lỗi, hiển thị message cho user |
| Parse JSON/data | Dùng `tryParse` hoặc `try-catch`, KHÔNG để crash |
| File I/O | Handle `FileSystemException` cụ thể |
| Navigation args | Validate params trước khi dùng |

### Pattern chuẩn

```dart
// ✅ Structured error handling
Future<Result<User>> fetchUser(String id) async {
  try {
    final response = await api.getUser(id);
    return Result.success(User.fromJson(response));
  } on DioException catch (e) {
    developer.log('API failed', name: 'user.fetch', error: e);
    return Result.failure(e.toAppError());
  } catch (e, s) {
    developer.log('Unexpected', name: 'user.fetch', error: e, stackTrace: s);
    return Result.failure(AppError.unexpected(e));
  }
}
```

### Cấm

| ❌ Sai | Lý do |
|--------|-------|
| `catch (e) {}` (empty catch) | Nuốt lỗi, debug nightmare |
| `print(e)` | Dùng `developer.log()` thay vì print |
| Throw generic `Exception('Error')` | Tạo custom exceptions có context |
| Ignore `StackTrace` | Luôn log cả `stackTrace` để debug |

> 🔴 **Mỗi `try` phải có `catch` có ý nghĩa.** Log + User message + Recovery action.