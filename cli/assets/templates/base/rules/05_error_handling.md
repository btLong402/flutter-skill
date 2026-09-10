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
| Async UI Loader / Dialog | BẮT BUỘC dùng `try-finally` để tắt loader (`hideLoader()`), chống kẹt UI vĩnh viễn |
| Fetch Data Màn hình | BẮT BUỘC có UI Error State kèm nút "Thử lại" (Retry), KHÔNG nuốt lỗi thành Empty State |
| Parse JSON/data | Dùng `tryParse` hoặc `try-catch`, KHÔNG để crash |
| File I/O | Handle `FileSystemException` cụ thể |
| Navigation args | Validate params trước khi dùng |

### Pattern chuẩn

#### 1. Xử lý tầng Data / Repository (Result pattern & Không fake success)
```dart
// ✅ Structured error handling
Future<Result<User>> fetchUser(String id) async {
  try {
    final response = await api.getUser(id);
    // ⚠️ KHÔNG FAKE SUCCESS: Phải kiểm tra status code và mã nghiệp vụ
    if (response.statusCode != 200 || response.data == null) {
      return Result.failure(AppError.server('Dữ liệu không hợp lệ'));
    }
    return Result.success(User.fromJson(response.data));
  } on DioException catch (e) {
    developer.log('API failed', name: 'user.fetch', error: e);
    return Result.failure(e.toAppError());
  } catch (e, s) {
    developer.log('Unexpected', name: 'user.fetch', error: e, stackTrace: s);
    return Result.failure(AppError.unexpected(e));
  }
}
```

#### 2. Xử lý tầng Presentation / Controller (Guaranteed UI Cleanup)
```dart
// ✅ Luôn dùng try-finally khi hiển thị loading/overlay/dialog
Future<void> onSubmit() async {
  try {
    showLoader(); // hoặc isLoading.value = true;
    final result = await repository.submitData();
    if (result.isSuccess) {
      showToastSuccess('Thao tác thành công');
      Get.back(); // hoặc Navigator.pop()
    } else {
      showToastError(result.error.message); // Không fake success!
    }
  } catch (e, s) {
    developer.log('Submit error', error: e, stackTrace: s);
    showToastError('Đã có lỗi xảy ra, vui lòng thử lại');
  } finally {
    hideLoader(); // BẮT BUỘC: Đảm bảo loader luôn đóng kể cả khi ném lỗi
  }
}
```

#### 3. Xử lý UI State & Retry Path (Không nuốt lỗi thành Empty State)
```dart
// ❌ CẤM: catch (e) { items.clear(); } -> User tưởng không có dữ liệu
// ✅ BẮT BUỘC: Lưu trạng thái lỗi để View hiển thị Error UI kèm nút Thử lại
Future<void> loadProducts() async {
  uiState.value = UiState.loading();
  try {
    final result = await repository.getProducts();
    if (result.isSuccess) {
      uiState.value = UiState.success(result.data);
    } else {
      uiState.value = UiState.error(
        message: result.error.message,
        onRetry: () => loadProducts(),
      );
    }
  } catch (e, s) {
    developer.log('Load products failed', error: e, stackTrace: s);
    uiState.value = UiState.error(
      message: 'Không thể tải danh sách sản phẩm',
      onRetry: () => loadProducts(),
    );
  }
}
```

### Cấm

| ❌ Sai | Lý do |
|--------|-------|
| `catch (e) {}` (empty catch) | Nuốt lỗi, debug nightmare |
| `print(e)` | Dùng `developer.log()` thay vì print |
| Mở loader nhưng tắt ở cuối `try` thiếu `finally` | Lỗi mạng / 500 làm loader kẹt vĩnh viễn, app treo cứng |
| Coi request không ném Exception là thành công | API có thể trả 200 kèm body lỗi hoặc mã nghiệp vụ thất bại |
| Nuốt lỗi thành Empty State (`items = []` khi fetch lỗi) | Làm người dùng hiểu lầm hệ thống không có dữ liệu thay vì đang lỗi kết nối |
| Chỉ log lỗi (`debugPrint`) mà không báo UI | Người dùng bấm tương tác nhưng không có phản hồi (Silent failure) |
| Throw generic `Exception('Error')` | Tạo custom exceptions có context |
| Ignore `StackTrace` | Luôn log cả `stackTrace` để debug |

> 🔴 **Mỗi `try` phải có `catch` có ý nghĩa.** Log + User message + Recovery action. Mọi UI loading overlay **BẮT BUỘC** tắt trong `finally`. Hiển thị lỗi rõ ràng trên UI kèm nút Thử lại.