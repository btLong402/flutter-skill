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
├── .shared/flutter-pro-max/          # Shared data & scripts
│   ├── data/                         # 14 CSV knowledge base files
│   └── scripts/                      # Python search script
├── SKILL.md                          # Main skill documentation
└── README.md                         # Installation guide
```

## Key Commands

```bash
# Search widgets/packages/patterns
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "<query>" --top 5

# Search charts
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "chart bar" --top 5

# Search typography
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "font Inter" --top 5

# Search UX guidelines
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "touch accessibility" --top 5

# With stack filter
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "<query>" --stack riverpod

# JSON output
python3 .claude/skills/flutter-pro-max/scripts/flutter_search.py "<query>" --json
```

## Technical Standards

- **Dart 3**: Records, Pattern Matching, Sealed Classes
- **Null Safety**: Sound null safety, avoid `!` operator
- **Performance**: `const`, `SizedBox` > `Container`
- **State**: Riverpod (default), Bloc (optional)
- **Architecture**: Clean Architecture, Feature-First
- **UX**: Touch targets 44x44px, WCAG contrast
