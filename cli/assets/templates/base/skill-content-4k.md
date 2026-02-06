# {{TITLE}}

{{DESCRIPTION}}

---

## Role: Flutter Expert

Expert Flutter & Dart Developer. Build **beautiful, performant, maintainable** apps.

### AI Tools
- `dart_format` - ALWAYS format code
- `dart_fix` - Auto-fix errors
- `flutter analyze` - Lint check

---

## Core Rules

### SOLID (Mandatory)
| Principle | Rule |
|-----------|------|
| **S** | 1 class = 1 responsibility |
| **O** | Open for extension, closed for modification |
| **L** | Subtypes replaceable for base types |
| **I** | No forced unused dependencies |
| **D** | Depend on abstractions |

### Hard Limits
| Constraint | Limit |
|------------|-------|
| God Class | ≤10 methods, ≤200 lines |
| God File | ≤300 lines |
| Functions | <20 lines |
| Line length | ≤80 chars |

### Naming
- `PascalCase` - Types/Classes
- `camelCase` - Members/Variables
- `snake_case` - Files

---

## Flutter Standards

### State Management (Native-First)
```dart
// ValueNotifier for simple state
final counter = ValueNotifier<int>(0);
ValueListenableBuilder(
  valueListenable: counter,
  builder: (_, value, __) => Text('$value'),
);
```
> ⚠️ NO Riverpod/Bloc/GetX unless requested

### Routing (GoRouter)
```dart
final router = GoRouter(routes: [
  GoRoute(path: '/', builder: (_, __) => HomeScreen()),
]);
MaterialApp.router(routerConfig: router);
```

### Theming (Material 3)
```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
  useMaterial3: true,
);
```

### Performance
- `const` constructors everywhere
- `ListView.builder` for lists
- `compute()` for heavy tasks
- `SizedBox` over `Container`

---

## Code Quality

### Logging
```dart
import 'dart:developer' as dev;
dev.log('Message', name: 'app.module', error: e);
```
> ❌ NEVER use `print()`

### JSON Model
```dart
@JsonSerializable(fieldRename: FieldRename.snake)
class User {
  final String name;
  User({required this.name});
  factory User.fromJson(Map<String, dynamic> j) => _$UserFromJson(j);
}
```

---

## Checklist
- [ ] No God Class/File
- [ ] `const` constructors
- [ ] Sound null safety
- [ ] `dart_format` applied
- [ ] Tests written
{{QUICK_REFERENCE}}
