---
description: Quy tắc đặt tên (Naming), Cấu trúc thư mục (Folder Structure), Quy chuẩn Git Commit
globs: lib/**/*.dart, test/**/*.dart
---

# Rule: Naming Conventions & Codebase Structure

> Kích hoạt: Khi tạo mới hoặc đổi tên files, classes, functions, biến hoặc cấu trúc thư mục

## 1. Nguyên Tắc Cốt Lõi

> **Tên gọi phải mang tính tự giải thích (Self-explanatory). Cấu trúc thư mục phải dễ đoán và nhất quán.**

---

## 2. Chính Sách Kiến Trúc (Architecture Policy)

- **Mặc định (Greenfield / Module mới):** Cấu trúc thư mục và đặt tên bắt buộc tuân thủ Feature-First Clean Architecture.
- **Bảo trì dự án cũ (Brownfield):** Giữ nguyên quy ước đặt tên đang dùng trong feature đó (MVC / MVVM / Layered), tuyệt đối không thực hiện đổi tên hàng loạt (Force rename) gây xung đột Git.
- **Tái cấu trúc tăng dần:** Chỉ chuẩn hóa tên file mới hoặc các file trực tiếp chỉnh sửa trong phạm vi nhiệm vụ.

---

## 3. Quy Ước Đặt Tên Chi Tiết (Naming Conventions)

| Thành phần | Quy ước (Case) | Ví dụ chuẩn | Ví dụ sai |
| :--- | :--- | :--- | :--- |
| **Files & Folders** | `snake_case` | `user_profile_page.dart` | `UserProfilePage.dart`, `userProfile.dart` |
| **Classes & Enums** | `PascalCase` | `UserProfilePage`, `AppTheme` | `user_profile_page`, `appTheme` |
| **Functions & Methods** | `camelCase` | `fetchUserProfile()`, `onTap()` | `FetchUser()`, `fetch_user()` |
| **Variables & Params** | `camelCase` | `userName`, `isLoading` | `user_name`, `IsLoading` |
| **Constants** | `camelCase` hoặc `SCREAMING_SNAKE` | `maxRetryCount`, `API_BASE_URL` | `Max_Retry` |
| **Private Fields/Methods**| Prefix `_` + `camelCase` | `_buildHeader()`, `_userList` | `buildHeader_()`, `privateUser` |
| **Enum Values** | `camelCase` | `UserRole.adminRole` hoặc `admin` | `UserRole.ADMIN_ROLE` |

---

## 4. Hậu Tố Tên File theo Tầng Kiến Trúc (Layer Suffixes)

Mọi file Dart đều phải có hậu tố phản ánh chính xác vai trò kiến trúc:

| Tầng kiến trúc | Hậu tố bắt buộc | Ví dụ chuẩn |
| :--- | :--- | :--- |
| **Màn hình (Page/Screen)** | `*_page.dart` | `login_page.dart`, `order_history_page.dart` |
| **Widget UI con** | `*_widget.dart` hoặc tên mô tả | `user_avatar.dart`, `price_tag_widget.dart` |
| **Dữ liệu (Model/DTO)** | `*_model.dart` / `*_dto.dart` | `user_model.dart`, `auth_response_dto.dart` |
| **Thực thể Domain (Entity)**| `*_entity.dart` | `user_entity.dart`, `product_item.dart` |
| **Kho dữ liệu (Repository)** | `*_repository.dart` | `user_repository.dart`, `i_user_repository.dart` |
| **Nguồn dữ liệu (DataSource)**| `*_data_source.dart` | `user_remote_data_source.dart` |
| **Nghiệp vụ (UseCase/Service)**| `*_use_case.dart` / `*_service.dart`| `get_user_profile_use_case.dart`, `auth_service.dart`|
| **Quản lý State (Notifier/Bloc)**| `*_notifier.dart` / `*_bloc.dart` | `cart_notifier.dart`, `auth_bloc.dart` |
| **Tiện ích mở rộng (Extension)**| `*_extension.dart` | `string_extension.dart`, `context_extension.dart` |

---

## 5. Cấu Trúc Thư Mục Chuẩn: Feature-First Clean Architecture

```
lib/
├── core/                         # Thành phần dùng chung toàn app
│   ├── constants/                # App constants, API endpoints
│   ├── network/                  # Http client (Dio), Interceptors
│   ├── theme/                    # AppTheme, Colors, TextStyles
│   ├── utils/                    # Helper functions, Formatters
│   └── widgets/                  # Reusable UI widgets (AppButton, AppTextField)
├── features/                     # Chia theo từng tính năng độc lập
│   ├── auth/
│   │   ├── data/                 # Repositories impl, DataSources, Models/DTOs
│   │   ├── domain/               # Entities, Repository Interfaces, UseCases
│   │   └── presentation/         # Pages, Sub-widgets, Notifiers/Controllers
│   └── profile/
└── main.dart                     # Khởi tạo app và runApp()
```

---

## 6. Quy Chuẩn Git Commit (Conventional Commits)

Format chuẩn: `<type>(<scope>): <mô tả ngắn gọn>`

| Type | Ý nghĩa và tình huống sử dụng |
| :--- | :--- |
| `feat` | Thêm một tính năng mới cho người dùng. |
| `fix` | Sửa một lỗi (bug) trong mã nguồn. |
| `refactor` | Tái cấu trúc mã nguồn (không thêm tính năng, không sửa lỗi). |
| `perf` | Cải thiện hiệu năng xử lý hoặc render. |
| `test` | Thêm mới hoặc chỉnh sửa các bài kiểm thử (Unit/Widget/Integration test). |
| `docs` | Chỉ cập nhật tài liệu hướng dẫn hoặc comment. |
| `chore` | Cập nhật cấu hình, dependencies hoặc công cụ build. |

> 🔴 **Quy tắc dứt điểm:** Khi phát hiện tên file hoặc class đặt sai quy chuẩn, **SỬA NGAY TẠI CHỖ**, không để tích tụ thành nợ kỹ thuật.