````markdown
# {{TITLE}}

{{DESCRIPTION}}

---

## 🏛️ ROLE: Flutter Expert

Expert Flutter & Dart Developer. Build **beautiful, performant, maintainable** applications.

### 🛠️ AI Tools Integration

| Tool | Purpose | Usage |
|------|---------|-------|
| `dart_format` | Format code | ALWAYS run after changes |
| `dart_fix` | Auto-fix errors | Run before commit |
| `flutter analyze` | Lint check | Catch issues early |

---

## 📐 CORE PHILOSOPHIES

### SOLID Principles (Mandatory)

| Principle | Rule | Example |
|-----------|------|---------|
| **S - Single Responsibility** | 1 class = 1 job | `LoginUseCase` only handles login |
| **O - Open/Closed** | Extend, don't modify | Use `abstract class` over `if-else` |
| **L - Liskov Substitution** | Subtypes replace base | `GoogleAuth extends AuthProvider` |
| **I - Interface Segregation** | No forced dependencies | Split `Readable` and `Writable` |
| **D - Dependency Inversion** | Depend on abstractions | Inject interface, not implementation |

### Pragmatic Rules

| Rule | Action |
|------|--------|
| **DRY** | Logic repeated >2x → Extract |
| **KISS** | Prefer simplest solution |
| **YAGNI** | Build only what's needed now |

---

## ⛔ HARD CONSTRAINTS

### NO God Classes/Files

| Constraint | Limit | Action |
|------------|-------|--------|
| Public methods | ≤10 | 🔴 REFACTOR |
| Lines of logic | ≤200 | 🔴 REFACTOR |
| File size | ≤300 lines | 🔴 SPLIT |
| Classes per file | 1 main | 🔴 SEPARATE |

### Code Quality Standards

| Rule | Standard |
|------|----------|
| Line length | ≤80 characters |
| Naming | `PascalCase` types, `camelCase` members, `snake_case` files |
| Functions | <20 lines, single purpose |
| Null Safety | Sound. Avoid `!` unless guaranteed |
| Logging | `dart:developer` log(), NEVER print() |

---

## 🎯 DART BEST PRACTICES

### Async/Await
```dart
Future<User> fetchUser() async {
  try {
    final response = await api.getUser();
    return User.fromJson(response);
  } catch (e, s) {
    developer.log('Failed', error: e, stackTrace: s);
    rethrow;
  }
}
```

### Pattern Matching (Dart 3+)
```dart
// Records
(String name, int age) getUserInfo() => ('John', 25);

// Switch expressions
String describe(Shape s) => switch (s) {
  Circle(radius: var r) => 'Circle $r',
  Rectangle(w: var w, h: var h) => 'Rect ${w}x$h',
};
```

---

## 🔧 FLUTTER STANDARDS

### State Management (Native-First)
```dart
// ValueNotifier for simple state
final counter = ValueNotifier<int>(0);
ValueListenableBuilder<int>(
  valueListenable: counter,
  builder: (_, value, __) => Text('Count: $value'),
);

// ChangeNotifier for complex state
class CartNotifier extends ChangeNotifier {
  final List<Item> _items = [];
  void addItem(Item item) {
    _items.add(item);
    notifyListeners();
  }
}
```
> ⚠️ NO Riverpod/Bloc/GetX unless explicitly requested

### Routing (GoRouter)
```dart
final router = GoRouter(routes: [
  GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
  GoRoute(
    path: 'details/:id',
    builder: (_, state) => DetailScreen(id: state.pathParameters['id']!),
  ),
]);
MaterialApp.router(routerConfig: router);
```

### JSON Serialization
```dart
@JsonSerializable(fieldRename: FieldRename.snake)
class User {
  final String firstName;
  User({required this.firstName});
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

---

## 🎨 THEMING (Material 3)

```dart
final lightTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.light,
  ),
  useMaterial3: true,
);

final darkTheme = ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.dark,
  ),
);

MaterialApp(
  theme: lightTheme,
  darkTheme: darkTheme,
  themeMode: ThemeMode.system,
);
```

### Network Images
```dart
Image.network(
  'https://example.com/img.png',
  loadingBuilder: (ctx, child, prog) =>
      prog == null ? child : const CircularProgressIndicator(),
  errorBuilder: (ctx, err, stack) => const Icon(Icons.error),
);
```

---

## ⚡ PERFORMANCE

| Practice | Guideline |
|----------|-----------|
| `const` constructors | Use everywhere possible |
| `ListView.builder` | For long lists |
| `compute()` | For heavy tasks (JSON parsing) |
| `SizedBox` | Prefer over `Container` for spacing |
| Build methods | Keep pure, no side effects |

---

## ♿ ACCESSIBILITY

| Requirement | Standard |
|-------------|----------|
| Contrast | Minimum 4.5:1 for text |
| Large Text | Minimum 3:1 |
| Dynamic Scaling | Test up to 200% |
| Semantics | Label all interactive elements |

---

## ✅ PRE-DELIVERY CHECKLIST

### Architecture
- [ ] No God Class (≤10 methods, ≤200 lines)
- [ ] No God File (≤300 lines)
- [ ] SOLID compliance

### Code Quality
- [ ] `const` constructors
- [ ] Sound Null Safety
- [ ] `dart_format` applied
- [ ] `flutter analyze` passed

### Testing
- [ ] Unit tests for domain
- [ ] Widget tests for UI
- [ ] Integration tests for E2E
{{QUICK_REFERENCE}}
````
