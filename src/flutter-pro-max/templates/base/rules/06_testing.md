---
description: Viết Unit Test, Widget Test, Integration Test
globs: test/**/*.dart, lib/**/*.dart
---

# Rule: Testing

> Kích hoạt: Khi tạo feature mới, fix bug, hoặc refactor logic

## Nguyên tắc: Không có test = Không hoàn thành

### Khi nào PHẢI viết test

| Loại code | Test bắt buộc | Ví dụ |
|-----------|---------------|-------|
| Business logic | Unit test | UseCase, Service, Validator |
| Repository/DataSource | Unit test với mock | API calls, DB queries |
| Widget có logic | Widget test | Form validation, state changes |
| User flow quan trọng | Integration test | Login, checkout, onboarding |

### Khi nào KHÔNG cần test

- Pure UI widget không có logic (chỉ layout/styling)
- Generated code (`.g.dart`, `.freezed.dart`)
- Constants, enums đơn giản

### Pattern chuẩn

```dart
// ✅ Test structure: Arrange → Act → Assert
test('should return user when API succeeds', () async {
  // Arrange
  when(mockApi.getUser('123')).thenAnswer(
    (_) async => {'name': 'John'},
  );

  // Act
  final result = await useCase.execute('123');

  // Assert
  expect(result, isA<Success<User>>());
  expect(result.data.name, equals('John'));
});
```

### Quy tắc

- File test đặt cùng tên: `user_service.dart` → `user_service_test.dart`
- Dùng `package:mocktail` hoặc `package:mockito` cho mocking
- Mỗi test case chỉ test 1 behavior
- Tên test mô tả behavior: `should [expected] when [condition]`

> 🔴 **Fix bug?** Viết test reproduce bug TRƯỚC, rồi mới fix.