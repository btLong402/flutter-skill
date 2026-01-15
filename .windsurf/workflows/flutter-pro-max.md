---
description: Flutter Pro Max - Chuyên gia Flutter với Clean Architecture và Performance
---

# flutter-pro-max

Searchable database của Flutter widgets, packages, design patterns, architecture guidelines, colors, typography, và best practices.

## Prerequisites

```bash
python3 --version
pip install rank-bm25
```

---

## How to Use This Workflow

Khi user yêu cầu Flutter work, follow workflow này:

### Step 1: Analyze User Requirements

Trích xuất thông tin từ request:
- **Architecture**: Clean Architecture, Feature-First, DDD
- **State Management**: Riverpod (default), Bloc, Provider
- **UI Components**: Widgets, Layouts, Animations
- **Design**: Colors, Typography, Styles
- **Package needs**: Networking, Database, Security, etc.

### Step 2: Search Relevant Data (14 Sources)

```bash
python3 .windsurf/workflows/scripts/search.py "<keyword>" --top 5
python3 .windsurf/workflows/scripts/search.py "<keyword>" --stack riverpod --top 5
```

**Available stacks:** `riverpod`, `bloc`, `provider`

**Search Examples by Domain:**
```bash
# Flutter Widgets
python3 .windsurf/workflows/scripts/search.py "ListView pagination" --top 5

# Design Patterns
python3 .windsurf/workflows/scripts/search.py "authentication login" --top 5

# Charts
python3 .windsurf/workflows/scripts/search.py "chart bar comparison" --top 5

# Typography
python3 .windsurf/workflows/scripts/search.py "font modern SaaS" --top 5

# Colors by Product
python3 .windsurf/workflows/scripts/search.py "fintech crypto dark" --top 5

# UX Guidelines
python3 .windsurf/workflows/scripts/search.py "touch target accessibility" --top 5

# UI Styles
python3 .windsurf/workflows/scripts/search.py "glassmorphism neumorphism" --top 5
```

### Step 3: Apply Technical Standards

#### Dart 3 Modern Syntax
```dart
// ✅ Records
(String name, int age) getUserInfo() => ('John', 25);

// ✅ Pattern Matching
String getMessage(UIState state) => switch (state) {
  LoadingState() => 'Loading...',
  DataState(data: var d) => 'Data: $d',
  ErrorState(message: var m) => 'Error: $m',
};
```

#### Performance Rules
- Luôn dùng `const` constructor khi có thể
- Ưu tiên `SizedBox` hơn `Container` cho spacing
- Dùng `ListView.builder` thay vì `ListView` + `children`

#### State Management
- **Default**: Riverpod với `riverpod_generator`
- **Alternative**: Bloc (khi user yêu cầu)

---

## Search Reference

### Available Data Sources (14 files)

| Type | File | Content |
|------|------|---------|
| Widget | `widget.csv` | 65+ Flutter widgets với pro-tips |
| Package | `package.csv` | 100+ packages với best practices |
| Pattern | `patterns.csv` | 100+ design patterns với code snippets |
| Architecture | `architect.csv` | Clean Architecture layer paths |
| Chart | `charts.csv` | Chart type recommendations by data |
| Color | `colors.csv` | Color palettes by product type |
| Typography | `typography.csv` | Font pairings với Google Fonts |
| Style | `styles.csv` | UI style guidelines (Glass, Neubrutalism...) |
| UX Guideline | `ux-guidelines.csv` | UX best practices (Do/Don't) |
| Icon | `icons.csv` | Icon recommendations |
| Landing | `landing.csv` | Landing page section patterns |
| Naming | `name_convention.csv` | Dart/Flutter naming conventions |
| Product | `products.csv` | Product type styling recommendations |
| Prompt | `prompts.csv` | AI prompt templates |

---

## Example Workflow

**User Request:** "Tạo màn hình đăng nhập với Riverpod"

1. **Search widgets:**
   ```bash
   python3 .windsurf/workflows/scripts/search.py "form input text field" --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 .windsurf/workflows/scripts/search.py "authentication login" --top 5
   ```

3. **Search packages:**
   ```bash
   python3 .windsurf/workflows/scripts/search.py "validation form" --stack riverpod --top 5
   ```

4. **Apply results** to generate code với Riverpod state management

---

## Pre-Delivery Checklist

### Code Quality
- [ ] Sử dụng `const` constructors
- [ ] Sound Null Safety (không dùng `!` bừa bãi)
- [ ] Dart 3 syntax (Records, Pattern Matching)

### Performance
- [ ] `ListView.builder` cho lists dài
- [ ] `SizedBox` thay vì `Container` cho spacing

### Architecture
- [ ] Tuân thủ Clean Architecture layers
- [ ] Repository pattern cho data access

### UX/UI
- [ ] Touch targets tối thiểu 44x44px
- [ ] Colors đúng với product type
- [ ] Typography phù hợp với brand
