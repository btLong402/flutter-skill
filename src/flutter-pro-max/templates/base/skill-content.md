# {{TITLE}}

{{DESCRIPTION}}

---

## Prerequisites

```bash
python3 --version || python --version
```

---

## How to Use This {{SKILL_OR_WORKFLOW}}

### Step 1: Analyze User Requirements

Trích xuất thông tin từ request:
- **Architecture**: Clean Architecture, Feature-First, DDD
- **State Management**: Riverpod, Bloc, Provider (hoặc native-first)
- **UI Components**: Widgets, Layouts, Animations

### Step 2: Search Relevant Data

```bash
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --top 5
```

**Với domain cụ thể:**
```bash
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --domain widget --top 5
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --domain package --top 5
```

**Với stack filter:**
```bash
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --stack riverpod --top 5
```

**JSON output:**
```bash
python3 {{SCRIPT_PATH}}/search.py "<keyword>" --json --top 5
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
python3 {{SCRIPT_PATH}}/search.py "google play store listing" --domain play-store --top 5
python3 {{SCRIPT_PATH}}/search.py "content rating data safety" --domain play-store --top 5
python3 {{SCRIPT_PATH}}/search.py "app name short description" --domain play-store --json --top 5
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

4. **Apply results** theo Agent Rules (consistency, error handling, testing...)

5. **Validate:**
   ```bash
   dart format . && flutter analyze . && flutter test .
   ```
{{QUICK_REFERENCE}}
