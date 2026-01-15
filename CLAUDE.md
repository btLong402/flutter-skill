# CLAUDE.md

## Project Overview

Flutter Pro Max là AI Skill cung cấp kiến thức Flutter chuyên sâu.

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

## Project Structure

```
.
├── .claude/skills/flutter-pro-max/   # Claude skill
├── .shared/                          # Shared resources
│   ├── data/                         # 14 CSV knowledge base files
│   └── flutter-pro-max/scripts/      # Python search scripts (core.py, search.py)
├── scripts/                          # Root scripts (source)
│   ├── core.py                       # BM25 search engine
│   └── search.py                     # CLI entry point
└── README.md                         # Installation guide
```

## Key Commands

```bash
# Auto-detect domain search
python3 scripts/search.py "<query>" --top 5

# Specific domain
python3 scripts/search.py "ListView" --domain widget --top 5
python3 scripts/search.py "dio http" --domain package --top 5

# With stack filter
python3 scripts/search.py "<query>" --stack riverpod --top 5

# JSON output
python3 scripts/search.py "<query>" --json --top 5
```

**Available domains:** `widget`, `package`, `pattern`, `architect`, `chart`, `color`, `typography`, `style`, `ux`, `icon`, `landing`, `naming`, `product`, `prompt`

**Available stacks:** `riverpod`, `bloc`, `provider`

## Technical Standards

- **Dart 3**: Records, Pattern Matching, Sealed Classes
- **Null Safety**: Sound null safety, avoid `!` operator
- **Performance**: `const`, `SizedBox` > `Container`
- **State**: Riverpod (default), Bloc (optional)
- **Architecture**: Clean Architecture, Feature-First
- **UX**: Touch targets 44x44px, WCAG contrast
