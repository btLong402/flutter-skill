# Rule: Naming & Conventions

> Kích hoạt: Khi tạo files, classes, functions, hoặc variables

## Nguyên tắc: Tên phải tự giải thích, cấu trúc phải nhất quán

### Naming Convention

| Element | Convention | Ví dụ |
|---------|-----------|-------|
| Files | `snake_case` | `user_profile_page.dart` |
| Classes | `PascalCase` | `UserProfilePage` |
| Functions/Methods | `camelCase` | `fetchUserProfile()` |
| Variables | `camelCase` | `userName`, `isLoading` |
| Constants | `camelCase` hoặc `SCREAMING_SNAKE` | `maxRetryCount`, `API_BASE_URL` |
| Private | Prefix `_` | `_buildHeader()`, `_items` |
| Enums | `PascalCase` values | `UserRole.admin` |

### File Naming theo Layer

| Layer | Pattern | Ví dụ |
|-------|---------|-------|
| Page/Screen | `*_page.dart` | `login_page.dart` |
| Widget | `*_widget.dart` hoặc tên mô tả | `user_avatar.dart` |
| Model | `*_model.dart` | `user_model.dart` |
| Repository | `*_repository.dart` | `auth_repository.dart` |
| Service/UseCase | `*_service.dart` / `*_use_case.dart` | `auth_service.dart` |
| Provider/Notifier | `*_provider.dart` / `*_notifier.dart` | `cart_notifier.dart` |
| Extension | `*_extension.dart` | `string_extension.dart` |

### Folder Structure

```
lib/
├── core/              # Shared: theme, utils, widgets, constants
│   ├── theme/
│   ├── widgets/       # Reusable widgets
│   ├── utils/
│   └── constants/
├── features/          # Feature-first organization
│   ├── auth/
│   │   ├── data/      # Repository implementations, models
│   │   ├── domain/    # Entities, use cases, repo interfaces
│   │   └── presentation/  # Pages, widgets, notifiers
│   └── home/
└── main.dart
```

### Git Commit Convention

```
<type>(<scope>): <description>

feat(auth): add biometric login support
fix(cart): resolve item count not updating
refactor(core): extract shared AppBar widget
docs(readme): update installation guide
test(auth): add login use case unit tests
```

| Type | Khi nào |
|------|---------|
| `feat` | Feature mới |
| `fix` | Sửa bug |
| `refactor` | Restructure code, không đổi behavior |
| `docs` | Documentation only |
| `test` | Thêm/sửa tests |
| `chore` | Config, dependencies, tooling |

> 🔴 **Đặt tên file/class sai convention?** Rename ngay, không để nợ.
