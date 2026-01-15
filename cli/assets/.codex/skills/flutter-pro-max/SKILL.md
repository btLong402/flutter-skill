---
name: flutter-pro-max
description: Chuyên gia Flutter với Clean Architecture, Performance, Dart 3
---

# Flutter Pro Max - Flutter Design Intelligence

Searchable database của Flutter widgets, packages, design patterns, colors, typography, và best practices.

## Prerequisites

```bash
pip install rank-bm25
```

---

## How to Use

### Step 1: Analyze Requirements
- **Architecture**: Clean Architecture, Feature-First
- **State**: Riverpod (default), Bloc
- **UI**: Widgets, Colors, Typography

### Step 2: Search (14 Sources)

```bash
python3 .codex/skills/flutter-pro-max/scripts/search.py "<keyword>" --top 5
python3 .codex/skills/flutter-pro-max/scripts/search.py "<keyword>" --stack riverpod --top 5
```

**Examples:**
```bash
# Widgets
python3 .codex/skills/flutter-pro-max/scripts/search.py "ListView pagination" --top 5

# Charts
python3 .codex/skills/flutter-pro-max/scripts/search.py "chart bar" --top 5

# Typography
python3 .codex/skills/flutter-pro-max/scripts/search.py "font modern SaaS" --top 5

# Colors
python3 .codex/skills/flutter-pro-max/scripts/search.py "fintech crypto" --top 5

# UX Guidelines  
python3 .codex/skills/flutter-pro-max/scripts/search.py "touch accessibility" --top 5
```

### Step 3: Apply Standards

#### Dart 3
```dart
// Records
(String name, int age) getUserInfo() => ('John', 25);

// Pattern Matching
String getMessage(UIState state) => switch (state) {
  LoadingState() => 'Loading...',
  DataState(data: var d) => 'Data: $d',
  ErrorState(message: var m) => 'Error: $m',
};
```

#### Performance
- `const` constructors
- `SizedBox` > `Container` for spacing
- `ListView.builder` for lists

---

## Data Sources (14 files)

| Type | File | Content |
|------|------|---------|
| Widget | `widget.csv` | 65+ widgets |
| Package | `package.csv` | 100+ packages |
| Pattern | `patterns.csv` | 100+ patterns |
| Architecture | `architect.csv` | Clean Architecture |
| Chart | `charts.csv` | Chart recommendations |
| Color | `colors.csv` | Color palettes |
| Typography | `typography.csv` | Font pairings |
| Style | `styles.csv` | UI styles |
| UX Guideline | `ux-guidelines.csv` | UX best practices |
| Icon | `icons.csv` | Icons |
| Landing | `landing.csv` | Landing patterns |
| Naming | `name_convention.csv` | Naming conventions |
| Product | `products.csv` | Product styling |
| Prompt | `prompts.csv` | AI prompts |

---

## Pre-Delivery Checklist

- [ ] `const` constructors
- [ ] Sound Null Safety
- [ ] Dart 3 syntax
- [ ] Clean Architecture
- [ ] Touch targets 44x44px
- [ ] WCAG contrast
