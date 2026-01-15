---
description: Flutter Pro Max - Chuyên gia Flutter với Clean Architecture và Performance
---

# flutter-pro-max

Searchable database: widgets, packages, patterns, colors, typography (14 files).

## Prerequisites

```bash
pip install rank-bm25
```

## Search (14 Sources)

```bash
python3 .roo/commands/scripts/search.py "<keyword>" --top 5
python3 .roo/commands/scripts/search.py "<keyword>" --stack riverpod --top 5
```

**Examples:**
```bash
# Widgets
python3 .roo/commands/scripts/search.py "ListView" --top 5

# Charts
python3 .roo/commands/scripts/search.py "chart bar" --top 5

# Typography
python3 .roo/commands/scripts/search.py "font modern" --top 5

# UX
python3 .roo/commands/scripts/search.py "touch accessibility" --top 5
```

## Data Sources (14 files)

| Type | File |
|------|------|
| Widget | `widget.csv` |
| Package | `package.csv` |
| Pattern | `patterns.csv` |
| Architecture | `architect.csv` |
| Chart | `charts.csv` |
| Color | `colors.csv` |
| Typography | `typography.csv` |
| Style | `styles.csv` |
| UX Guideline | `ux-guidelines.csv` |
| Icon | `icons.csv` |
| Landing | `landing.csv` |
| Naming | `name_convention.csv` |
| Product | `products.csv` |
| Prompt | `prompts.csv` |

## Standards
- Dart 3, Performance, Riverpod (default)
- UX: Touch targets 44x44px
