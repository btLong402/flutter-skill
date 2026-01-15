---
description: Chuyên gia Flutter với kiến thức sâu về Clean Architecture, Performance và Modern Dart 3
---

# Flutter Pro Max - Flutter Design Intelligence

Searchable database của Flutter widgets, packages, design patterns, architecture guidelines, và best practices.

## Prerequisites

Chỉ cần Python (không cần pip install):

```bash
python3 --version || python --version
```

---

## How to Use This Steering

Khi user yêu cầu Flutter work (design, build, create, implement, review, fix, improve), follow workflow này:

### Step 1: Analyze User Requirements

Trích xuất thông tin từ request:
- **Architecture**: Clean Architecture, Feature-First, DDD
- **State Management**: Riverpod (default), Bloc, Provider
- **UI Components**: Widgets, Layouts, Animations
- **Package needs**: Networking, Database, Security, etc.

### Step 2: Search Relevant Data

Sử dụng `search.py` để tìm kiếm (auto-detect domain):

```bash
python3 .kiro/steering/scripts/search.py "<keyword>" --top 5
```

**Với domain cụ thể:**
```bash
python3 .kiro/steering/scripts/search.py "<keyword>" --domain widget --top 5
python3 .kiro/steering/scripts/search.py "<keyword>" --domain package --top 5
```

**Với stack filter (loại bỏ conflicts):**
```bash
python3 .kiro/steering/scripts/search.py "<keyword>" --stack riverpod --top 5
```

**Available domains:** `widget`, `package`, `pattern`, `architect`, `chart`, `color`, `typography`, `style`, `ux`, `icon`, `landing`, `naming`, `product`, `prompt`

**Available stacks:** `riverpod`, `bloc`, `provider`

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

### Available Data

| Domain | File | Content |
|--------|------|---------|
| Widgets | `widget.csv` | 65+ Flutter widgets với pro-tips |
| Packages | `package.csv` | 100+ packages với best practices |
| Patterns | `patterns.csv` | 100+ design patterns với code snippets |
| Architecture | `architect.csv` | Clean Architecture layer paths |
| Charts | `charts.csv` | Chart type recommendations |
| Colors | `colors.csv` | Color palettes by product type |
| Typography | `typography.csv` | Font pairings |
| Styles | `styles.csv` | UI style guidelines |
| UX Guidelines | `ux-guidelines.csv` | UX best practices |
| Icons | `icons.csv` | Icon recommendations |
| Landing | `landing.csv` | Landing page patterns |
| Naming | `name_convention.csv` | Naming conventions |
| Products | `products.csv` | Product type styling |
| Prompts | `prompts.csv` | AI prompt templates |

### Search Examples

```bash
# Auto-detect domain
python3 .kiro/steering/scripts/search.py "ListView" --top 5

# Specific domain
python3 .kiro/steering/scripts/search.py "network http" --domain package --top 5

# Stack filter
python3 .kiro/steering/scripts/search.py "state" --stack riverpod --top 5

# JSON output
python3 .kiro/steering/scripts/search.py "login" --json --top 3
```

---

## Example Workflow

**User Request:** "Tạo màn hình đăng nhập với Riverpod"

1. **Search widgets:**
   ```bash
   python3 .kiro/steering/scripts/search.py "form input" --domain widget --top 5
   ```

2. **Search patterns:**
   ```bash
   python3 .kiro/steering/scripts/search.py "authentication login" --domain pattern --top 5
   ```

3. **Search packages:**
   ```bash
   python3 .kiro/steering/scripts/search.py "validation" --domain package --stack riverpod --top 5
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
- [ ] `const` widgets được đánh dấu

### Architecture
- [ ] Tuân thủ Clean Architecture layers
- [ ] Dependency Injection đúng cách
- [ ] Repository pattern cho data access

### State Management
- [ ] Riverpod providers được tổ chức hợp lý
- [ ] Không leak state giữa các features
- [ ] Error handling với AsyncValue
