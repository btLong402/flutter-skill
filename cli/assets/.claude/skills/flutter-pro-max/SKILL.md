---
name: flutter-pro-max
description: Chuyên gia Flutter với kiến thức sâu về Clean Architecture, Performance và Modern Dart 3
---

# Flutter Pro Max - Flutter Design Intelligence

Searchable database của Flutter widgets, packages, design patterns, architecture guidelines, và best practices.

## Prerequisites

Kiểm tra Python đã cài đặt:

```bash
python3 --version || python --version
```

Cài đặt dependency:

```bash
pip install rank-bm25
```

---

## How to Use This Skill

Khi user yêu cầu Flutter work (design, build, create, implement, review, fix, improve), follow workflow này:

### Step 1: Analyze User Requirements

Trích xuất thông tin từ request:
- **Architecture**: Clean Architecture, Feature-First, DDD
- **State Management**: Riverpod (default), Bloc, Provider
- **UI Components**: Widgets, Layouts, Animations
- **Design**: Colors, Typography, Styles
- **Package needs**: Networking, Database, Security, etc.

### Step 2: Search Relevant Data

Sử dụng `flutter_search.py` để tìm kiếm trong **14 data sources**:

```bash
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "<keyword>" --top 5
```

**Với stack filter (loại bỏ conflicts):**
```bash
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "<keyword>" --stack riverpod --top 5
```

**Available stacks:** `riverpod`, `bloc`, `provider`

**Search Examples by Domain:**
```bash
# Flutter Widgets
python3 scripts/flutter_search.py "ListView pagination" --top 5

# Design Patterns
python3 scripts/flutter_search.py "authentication login" --top 5

# Charts
python3 scripts/flutter_search.py "chart bar comparison" --top 5

# Typography
python3 scripts/flutter_search.py "font modern SaaS" --top 5

# Colors by Product
python3 scripts/flutter_search.py "fintech crypto dark" --top 5

# UX Guidelines
python3 scripts/flutter_search.py "touch target accessibility" --top 5

# UI Styles
python3 scripts/flutter_search.py "glassmorphism neumorphism" --top 5
```

### Step 3: Apply Technical Standards

Luôn tuân thủ các tiêu chuẩn:

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
   python3 scripts/flutter_search.py "form input text field" --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 scripts/flutter_search.py "authentication login" --top 5
   ```

3. **Search packages:**
   ```bash
   python3 scripts/flutter_search.py "validation form" --stack riverpod --top 5
   ```

4. **Search colors:**
   ```bash
   python3 scripts/flutter_search.py "saas professional" --top 3
   ```

5. **Apply results** to generate code với Riverpod state management

---

## Pre-Delivery Checklist

### Code Quality
- [ ] Sử dụng `const` constructors
- [ ] Sound Null Safety (không dùng `!` bừa bãi)
- [ ] Dart 3 syntax (Records, Pattern Matching)

### Performance
- [ ] `ListView.builder` cho lists dài
- [ ] `SizedBox` thay vì `Container` cho spacing
- [ ] `const` widgets được đánh dấu

### Architecture
- [ ] Tuân thủ Clean Architecture layers
- [ ] Dependency Injection đúng cách
- [ ] Repository pattern cho data access

### State Management
- [ ] Riverpod providers được tổ chức hợp lý
- [ ] Không leak state giữa các features
- [ ] Error handling với AsyncValue

### UX/UI
- [ ] Touch targets tối thiểu 44x44px
- [ ] Colors đúng với product type
- [ ] Typography phù hợp với brand
