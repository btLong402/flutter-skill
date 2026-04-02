
## Quick Reference

### AI Tools Commands

```bash
# Format code (ALWAYS run after changes)
dart format .

# Auto-fix common issues
dart fix --apply

# Analyze with lints
flutter analyze .

# Run tests
flutter test .

# Build runner for code generation
dart run build_runner build --delete-conflicting-outputs
```

### Search Commands

```bash
# Auto-detect domain
python3 {{SCRIPT_PATH}}/search.py "ListView" --top 5

# Specific domain
python3 {{SCRIPT_PATH}}/search.py "network http" --domain package --top 5

# Stack filter (native-first: valuenotifier, changenotifier)
python3 {{SCRIPT_PATH}}/search.py "state" --stack provider --top 5

# JSON output
python3 {{SCRIPT_PATH}}/search.py "login" --json --top 3

# Google Play Console workflow
python3 {{SCRIPT_PATH}}/search.py "google play listing" --domain play-store --top 5
python3 {{SCRIPT_PATH}}/search.py "data safety content rating" --domain play-store --json --top 5
```

### Package Management

```bash
# Add dependency
flutter pub add <package_name>

# Add dev dependency
flutter pub add dev:<package_name>

# Add override
flutter pub add override:<package_name>:<version>

# Remove dependency
dart pub remove <package_name>
```

### Example Workflow

**User Request:** "Tạo màn hình đăng nhập"

1. **Search widgets:**
   ```bash
   python3 {{SCRIPT_PATH}}/search.py "form input" --domain widget --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 {{SCRIPT_PATH}}/search.py "authentication login" --domain pattern --top 5
   ```

3. **Search packages:**
   ```bash
   python3 {{SCRIPT_PATH}}/search.py "validation" --domain package --top 5
   ```

4. **Apply results** với native state management (ValueNotifier/ChangeNotifier)

### Google Play Console Workflow

1. Search `play-store` for ASO, listing copy, and compliance guidance.
2. Generate text assets with the correct limits before writing anything final.
3. Validate content rating, data safety, screenshots, and privacy policy details.
4. Export Markdown for humans and JSON for machine-readable handoff.

5. **Validate:**
   ```bash
   dart format . && flutter analyze . && flutter test .
   ```

### Quick Code Templates

```dart
// Structured Logging (use instead of print)
import 'dart:developer' as developer;
developer.log('Message', name: 'app.module', error: e, stackTrace: s);

// JSON Model
@JsonSerializable(fieldRename: FieldRename.snake)
class User {
  final String firstName;
  User({required this.firstName});
  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// GoRouter Setup
final _router = GoRouter(routes: [
  GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
]);
MaterialApp.router(routerConfig: _router);
```
