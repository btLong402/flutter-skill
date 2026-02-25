# {{TITLE}}

{{DESCRIPTION}}

---

## How to Use

### Search

```bash
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --top 5
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --domain widget --top 5
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --stack riverpod --top 5
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --json --top 5
```

**Domains (17):** `widget`, `package`, `pattern`, `architect`, `chart`, `color`, `typography`, `style`, `ux`, `icon`, `landing`, `naming`, `product`, `prompt`, `performance`, `ui-reasoning`, `accessibility`

**Stacks:** `riverpod`, `bloc`, `provider`

### Search Reference

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

### Tools

```bash
dart format .               # Format code
dart fix --apply             # Auto-fix
flutter analyze .            # Lint check
flutter test .               # Run tests
```
{{QUICK_REFERENCE}}
