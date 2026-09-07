---
name: flutter-pro-max
description: "Flutter design intelligence. Widgets, packages, patterns, architecture, performance optimization, accessibility, and UI/UX best practices. Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, check Flutter code."
---
# Flutter Pro Max - Flutter Design Intelligence

Comprehensive Flutter development guide with searchable database of widgets, packages, design patterns, architecture guidelines, performance optimization, accessibility, and UI/UX best practices.

---

## Prerequisites

```bash
python3 --version || python --version
```

---

## How to Use This Skill

### Step 1: Analyze User Requirements

Trích xuất thông tin từ request:
- **Architecture**: Clean Architecture, Feature-First, DDD
- **State Management**: Riverpod, Bloc, Provider (hoặc native-first)
- **UI Components**: Widgets, Layouts, Animations

### Step 2: Search Relevant Data

```bash
python3 skills/flutter-pro-max/scripts/search.py "<keyword>" --top 5
```

**Với domain cụ thể:**
```bash
python3 skills/flutter-pro-max/scripts/search.py "<keyword>" --domain widget --top 5
python3 skills/flutter-pro-max/scripts/search.py "<keyword>" --domain package --top 5
```

**Với stack filter:**
```bash
python3 skills/flutter-pro-max/scripts/search.py "<keyword>" --stack riverpod --top 5
```

**JSON output:**
```bash
python3 skills/flutter-pro-max/scripts/search.py "<keyword>" --json --top 5
```

**Available domains (18):** `widget`, `package`, `pattern`, `architect`, `chart`, `color`, `typography`, `style`, `ux`, `icon`, `landing`, `naming`, `product`, `prompt`, `play-store`, `performance`, `ui-reasoning`, `accessibility`

**Available stacks:** `riverpod`, `bloc`, `provider`

### Step 3: Apply Results

Áp dụng kết quả search vào code theo các Agent Rules đã cài đặt.

---

## Search Reference

| Domain | File | Content |
|--------|------|---------|
| Widgets | `widget.csv` | 65+ Flutter widgets |
| Packages | `package.csv` | 100+ packages |
| Patterns | `patterns.csv` | 100+ design patterns |
| Architecture | `architect.csv` | Clean Architecture layers |
| Performance | `flutter-performance.csv` | 35+ performance patterns |
| Accessibility | `mobile-accessibility.csv` | 35+ accessibility patterns |
| UI Reasoning | `ui-reasoning.csv` | 35+ UI decision rules |
| Charts | `charts.csv` | Chart recommendations |
| Colors | `colors.csv` | Color palettes |
| Typography | `typography.csv` | Font pairings |
| Styles | `styles.csv` | UI style guidelines |
| UX Guidelines | `ux-guidelines.csv` | UX best practices |
| Icons | `icons.csv` | Icon recommendations |
| Landing | `landing.csv` | Landing page patterns |
| Naming | `name_convention.csv` | Naming conventions |
| Products | `products.csv` | Product type styling |
| Prompts | `prompts.csv` | AI prompt templates |
| Play Store | `play-store.csv` | ASO, store listing, compliance, privacy |

---

## Google Play Console Workflow

Use the `play-store` domain when the user asks for ASO, app listing copy, content rating, data safety, screenshots, privacy policy, or Play Console export.

### Suggested Flow

1. Analyze the app input and extract USP, persona, keywords, category, and tags.
2. Generate store text assets with strict length limits.
3. Validate compliance details for content rating, data safety, and privacy.
4. Produce screenshot and feature graphic guidance.
5. Export the result as Markdown and JSON when needed.

### Example Queries

```bash
python3 skills/flutter-pro-max/scripts/search.py "google play store listing" --domain play-store --top 5
python3 skills/flutter-pro-max/scripts/search.py "content rating data safety" --domain play-store --top 5
python3 skills/flutter-pro-max/scripts/search.py "app name short description" --domain play-store --json --top 5
```

### Output Targets

- App Name: max 30 characters, brand + core keyword
- Short Description: max 80 characters, concise value proposition
- Full Description: max 4000 characters, structured and policy-safe
- Compliance Pack: content rating answers, data safety table, privacy notes
- Visual Pack: first screenshot guidance, feature graphic, icon rules

## Example Workflow

**User Request:** "Tạo màn hình đăng nhập"

1. **Search widgets:**
   ```bash
   python3 skills/flutter-pro-max/scripts/search.py "form input" --domain widget --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 skills/flutter-pro-max/scripts/search.py "authentication login" --domain pattern --top 5
   ```

3. **Search packages:**
   ```bash
   python3 skills/flutter-pro-max/scripts/search.py "validation" --domain package --top 5
   ```

4. **Apply results** theo Agent Rules (consistency, error handling, testing...)

5. **Validate:**
   ```bash
   dart format . && flutter analyze . && flutter test .
   ```


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
python3 skills/flutter-pro-max/scripts/search.py "ListView" --top 5

# Specific domain
python3 skills/flutter-pro-max/scripts/search.py "network http" --domain package --top 5

# Stack filter (native-first: valuenotifier, changenotifier)
python3 skills/flutter-pro-max/scripts/search.py "state" --stack provider --top 5

# JSON output
python3 skills/flutter-pro-max/scripts/search.py "login" --json --top 3

# Google Play Console workflow
python3 skills/flutter-pro-max/scripts/search.py "google play listing" --domain play-store --top 5
python3 skills/flutter-pro-max/scripts/search.py "data safety content rating" --domain play-store --json --top 5
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
   python3 skills/flutter-pro-max/scripts/search.py "form input" --domain widget --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 skills/flutter-pro-max/scripts/search.py "authentication login" --domain pattern --top 5
   ```

3. **Search packages:**
   ```bash
   python3 skills/flutter-pro-max/scripts/search.py "validation" --domain package --top 5
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

