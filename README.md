# ⚡ Flutter Pro Max

**Expert architectural intelligence for building high-performance, scalable, and modern Flutter applications.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Flutter](https://img.shields.io/badge/Flutter-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart_3-0175C2?logo=dart&logoColor=white)](https://dart.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

[Overview](#-overview) | [Features](#-features) | [Installation](#-installation) | [Usage](#-usage) | [Supported Assistants](#-supported-ai-assistants) | [Changelog](CHANGELOG.md)

---

## 🌟 Overview

**Flutter Pro Max** là một lớp AI Intelligence chuyên sâu dành cho phát triển Flutter hiện đại, được xây dựng dựa trên [Flutter AI Rules](https://docs.flutter.dev/ai/ai-rules) chính thức. Nó cung cấp cho các AI coding assistant một cơ sở kiến thức khổng lồ về các kiến trúc (Clean Architecture, Feature-First), Native-First state management (ValueNotifier, ChangeNotifier), tối ưu hóa hiệu năng, tiêu chuẩn bảo mật và các patterns thiết kế UI/UX cao cấp.

Dù bạn đang xây dựng một ứng dụng Fintech phức tạp, một sàn thương mại điện tử quy mô lớn hay một SaaS Dashboard, skill này đảm bảo AI partner của bạn sẽ đưa ra các khuyến nghị cấp độ chuyên gia dựa trên các tiêu chuẩn công nghiệp mới nhất.

---

## 🧠 Architecture: Rules (Brain) + Skill (Hands)

Flutter Pro Max tách biệt hoàn toàn **logic ra quyết định** và **công cụ thực thi**:

| Layer | Vai trò | Nội dung |
|-------|---------|----------|
| **🧠 Rules (Brain)** | System prompt, persona, constraints | 22 modular rule files — định nghĩa cách suy nghĩ, giới hạn an toàn, luồng quyết định |
| **🤲 Skill (Hands)** | Tools, search, data access | Search commands, 18 domain data files, design system generator, design review agent |

### 🧠 22 Modular Rules — Comprehensive Guidebook

Hệ thống được thiết kế với **22 module rules** chuyên biệt, bao quát toàn diện mọi khía cạnh từ Code Quality đến Product Release. Mỗi file tích hợp sẵn tính năng tự động kích hoạt thông qua **YAML Frontmatter (MDC format)**.

**Tier 1: Foundation Rules (Bắt buộc)**
```
├── 01_skill_usage                # Bắt buộc: Tự động filter & áp dụng skill
├── 02_code_quality               # Tiêu chuẩn God files & logic leakage
├── 03_interaction_flow           # Luồng Tương tác "ABCR"
├── 04_app_consistency            # Design tokens & UX consistency
└── 05_error_handling             # Result pattern & Try-Catch
```

**Tier 2: Code Quality Rules**
```
├── 06_testing                    # Mocking, Unit & Widget test
├── 07_performance                # const, ListView.builder, OOM prevention
├── 08_security                   # Storage, Interceptor, APIs, Data Protection
├── 09_state_management           # Native-first hierarchy, Architecture-aware
└── 10_naming_conventions         # Conventions, directory structure
```

**Tier 3: UX & Resilience Rules**
```
├── 11_accessibility              # Contrast 4.5:1, Semantics, Touch targets 48x48px
├── 12_network_resiliency         # Exponential Backoff, Circuit Breaker
├── 13_offline_first              # Caching strategies, Background sync
├── 14_ui_graceful_degradation    # Fallbacks UI, Image error handling
└── 15_state_lifecycle            # Orientation change, Memory warning
```

**Tier 4: Architecture & Store Delivery**
```
├── 16_google_play_aso            # ASO: Store listing, Keywords optimization
├── 17_google_play_compliance     # Content rating, Data safety, Privacy policy
├── 18_google_play_visuals        # Screenshots, Feature graphics, Icon guidance
├── 19_architecture_decision_matrix # Greenfield vs Brownfield strategies
└── 20_development_workflow       # 8-step SDLC flow từ Requirement đến Polish
```

**Tier 5: Navigation & Internationalization**
```
├── 21_navigation_governance      # GoRouter, Type-Safe Routes, Deep Linking, Auth Guards
└── 22_localization               # Đa ngôn ngữ l10n, ARB files, Zero Hardcoded Strings
```

**🔥 Đột phá cho người dùng Cursor/Windsurf:** Khi khởi tạo, CLI tự động xuất sang định dạng `.mdc`. AI của bạn giờ đây có thể tự động đọc YAML frontmatter từ file `.mdc` để biết chính xác lúc nào nên nạp rule nào vào buffer (dựa trên tên file/context).

> 📖 **Reference:** [Flutter AI Rules](https://docs.flutter.dev/ai/ai-rules)

---

## 🚀 Features

Hệ thống kiến thức được xây dựng trên dữ liệu có cấu trúc bao quát hơn **180+ thành phần**:

- **🎛️ Design Dials (`--variance`, `--motion`, `--density`)** *(NEW)*: Tinh chỉnh linh hoạt biên độ sáng tạo, cường độ hoạt họa và mật độ giao diện (ánh xạ trực tiếp vào `VisualDensity` và `AppSpacing`).
- **🐦 Production Dart Theme Generator (`--export-dart`)** *(NEW)*: Xuất trực tiếp mã nguồn `app_theme.dart` theo chuẩn Material 3 với 3-Layer Tokens (`AppColors`, `AppSpacing`, `AppRadius`, `ColorScheme`, `ThemeExtension<AppCustomTokens>`).
- **🎬 Flutter Motion & Micro-interactions** *(NEW)*: Thư viện hoạt họa chuyên sâu (`flutter-motion.csv`) phân tầng Subtle, Standard, Complex với code Flutter chuẩn và chỉ dẫn GPU/Accessibility (`MediaQuery.disableAnimationsOf`).
- **🛡️ Deterministic Reasoning Contract** *(NEW)*: Closed-grammar reasoning engine (`reasoning_contract.py`) xử lý quy tắc quyết định không lỗi, loại bỏ hoàn toàn AI hallucination.
- **🔍 Flutter Design Review Agent & Command** *(NEW)*: Subagent `@flutter-design-review` và lệnh `/flutter-review` thực hiện audit 6 pha (RenderFlex overflow, touch target $\ge 48\text{ dp}$, font scaling `TextScaler`, theming, const hygiene).
- **🛠️ Developer Utility Tools (`makefile`, `fastlane`, `gitignore`)** *(NEW)*: Bộ công cụ tạo nhanh `Makefile` chuẩn hóa workflows, cấu hình `Fastlane` tự động hóa CI/CD (TestFlight & Google Play) và tự động quản lý `.gitignore` ngăn rò rỉ skill assets.
- **🎯 Intelligent Design System Generator**: Tự động sinh complete design system (colors, typography, spacing, patterns) dựa trên app category với reasoning engine.
- **🏛️ Architecture Excellence**: Clean Architecture, Feature-First, DDD, Repository Pattern, và Modular Design.
- **📱 Premium UI/UX Patterns**: 100+ design patterns có sẵn code snippets cho Glassmorphism, Neumorphism, Modern SaaS, và eCommerce.
- **📦 Smart Package Selection**: Hướng dẫn sử dụng 100+ packages phổ biến (Dio, Riverpod, Drift, Isar) với best practices và tránh xung đột stack.
- **⚡ Performance Optimization**: 35+ patterns tối ưu render, memory, isolate, animation với code examples.
- **♿ Mobile Accessibility**: 35+ patterns cho semantics, touch targets, contrast, focus management.
- **🧠 UI Reasoning**: 35+ app categories với decision rules cho style, color, typography phù hợp.
- **🛡️ Security & Integrity**: Tiêu chuẩn bảo mật API, lưu trữ dữ liệu an toàn và xử lý Null Safety triệt để.
- **🎨 Design System Integration**: Tích hợp sẵn bảng màu (Color Palettes), Typography pairings và bộ Icon phù hợp cho từng loại sản phẩm.
- **📏 Standards & Conventions**: Pre-defined naming conventions cho project lớn và cách tổ chức folder chuẩn mực.

---

## 📦 Installation

### The Quick Way (Recommended)

Khởi tạo project của bạn với CLI chính thức. Nó sẽ tự động nhận diện môi trường và cài đặt skill cho các AI assistant bạn đang dùng.

```bash
npx flutter-pro-max-cli
```

### Global Installation

Sử dụng cho nhiều dự án khác nhau:

```bash
# Cài đặt global
npm install -g flutter-pro-max-cli

# Khởi tạo trong bất kỳ project nào
flutter-pro-max init

# Cài đặt cho AI assistant cụ thể
flutter-pro-max init --ai claude
flutter-pro-max init --ai cursor
flutter-pro-max init --ai antigravity
```

### Other Commands

```bash
# Xem các phiên bản có sẵn
flutter-pro-max versions

# Cập nhật lên phiên bản mới nhất
flutter-pro-max update
```

---

## 🤖 Supported AI Assistants

Triển khai **Flutter Pro Max** vào toàn bộ workflow phát triển của bạn (16 platforms):

| Assistant | Install Type | Structure | Rules File |
|-----------|--------------|-----------|------------|
| **Claude Code** | Full | `.claude/skills/flutter-pro-max/` | `CLAUDE.md` (append) |
| **Codex** | Full | `.codex/skills/flutter-pro-max/` | `.codex/rules/` |
| **Continue** | Full | `.continue/skills/flutter-pro-max/` | `.continue/rules/` |
| **Antigravity** | Full | `.agents/skills/flutter-pro-max/` | `.agents/rules/` |
| **Gemini CLI** | Full | `.gemini/skills/flutter-pro-max/` | `.gemini/rules/` |
| **OpenCode** | Full | `.opencode/skills/flutter-pro-max/` | `.opencode/rules/` |
| **CodeBuddy** | Full | `.codebuddy/skills/flutter-pro-max/` | `.codebuddy/rules/` |
| **Trae** | Full | `.trae/skills/flutter-pro-max/` | `.trae/rules/` |
| **Junie** | Full | `.junie/skills/flutter-pro-max/` | `.junie/rules/` |
| **VS Code** | Full | `.vscode/skills/flutter-pro-max/` | `.vscode/rules/` |
| **Cursor** | Reference | `.cursor/commands/` + `.shared/` | `.cursor/rules/` |
| **Windsurf** | Reference | `.windsurf/skills/` + `.shared/` | `.windsurf/rules/` |
| **GitHub Copilot** | Reference | `.github/prompts/` + `.shared/` | `copilot-instructions.md` (append) |
| **Kiro** | Reference | `.kiro/steering/` + `.shared/` | `.kiro/rules/` |
| **Qoder** | Reference | `.qoder/skills/` + `.shared/` | `.qoder/rules/` |
| **Roo Code** | Reference | `.roo/commands/` + `.shared/` | `.roo/rules/` |

**Install Types:**
- **Full**: Data và scripts nằm trong skill folder (standalone)
- **Reference**: Skill file trỏ đến `.shared/` folder chung (tiết kiệm dung lượng)
- **Rules File**: Agent behavior rules được generate **tách biệt** khỏi skill content

---

## � Development & CLI Sync

### When Adding/Updating Rules

Khi bạn thêm hoặc cập nhật rules, **cần sync từ source đến CLI assets**:

**Source of Truth:** `src/flutter-pro-max/templates/base/rules/` ← Chỉnh sửa ở đây

**Steps:**

1. **Tạo/sửa rule file** trong `src/flutter-pro-max/templates/base/rules/`:
   ```bash
   # Ví dụ: Thêm rule mới
   vim src/flutter-pro-max/templates/base/rules/21_new_rule.md
   ```

2. **Sync ngay vào CLI assets** (bắt buộc trước khi commit):
   ```bash
   # Sync chỉ rules
   cp -r src/flutter-pro-max/templates/base/rules/* cli/assets/templates/base/rules/
   
   # Hoặc sync toàn bộ assets (data + scripts + templates)
   cp -r src/flutter-pro-max/data/* cli/assets/data/
   cp -r src/flutter-pro-max/scripts/* cli/assets/scripts/
   cp -r src/flutter-pro-max/templates/* cli/assets/templates/
   ```

3. **Commit & Push**:
   ```bash
   git add src/flutter-pro-max/templates/base/rules/
   git add cli/assets/templates/base/rules/
   git commit -m "feat: add rule 21 - [description]"
   ```

4. **Before Publishing CLI** (trong workflow npm publish):
   - Verify tất cả 20 rules đã sync vào `cli/assets/templates/base/rules/`
   - Bump version trong `cli/package.json`
   - Workflow tự động publish

> ⚠️ **CRITICAL:** Nếu không sync CLI assets, users sẽ không nhận được rules mới khi chạy `flutter-pro-max init`

---

## �🛠️ Usage

### Skill Mode (Auto-activate)

**Supported:** Claude Code, Codex, Continue, Antigravity, Gemini CLI, OpenCode, CodeBuddy, Trae

Skill tự động kích hoạt khi bạn yêu cầu các task liên quan đến Flutter. Just chat naturally:

```
Tạo màn hình Dashboard với Clean Architecture và Riverpod
```

> **Trae**: Switch to **SOLO** mode first. The skill will activate for Flutter requests.

### Workflow Mode (Slash Command)

**Supported:** Cursor, Windsurf, GitHub Copilot, Kiro, Qoder, Roo Code

Sử dụng slash command để gọi skill:

```
/flutter-pro-max Tạo màn hình Dashboard với Clean Architecture và Riverpod
```

### Search Script (Advanced)

Bạn cũng có thể gọi search script trực tiếp:

```bash
# Auto-detect domain
python3 src/flutter-pro-max/scripts/search.py "ListView pagination" --top 5

# Tìm theo domain cụ thể
python3 src/flutter-pro-max/scripts/search.py "const rebuild" --domain performance --top 5
python3 src/flutter-pro-max/scripts/search.py "banking app" --domain ui-reasoning --top 3
python3 src/flutter-pro-max/scripts/search.py "touch target" --domain accessibility --top 3
python3 src/flutter-pro-max/scripts/search.py "hero transition" --domain motion --top 3

# Tìm kiếm theo stack (loại bỏ packages xung đột)
python3 src/flutter-pro-max/scripts/search.py "state management" --stack riverpod --top 5
```

### Available Search Domains (18 total)

| Domain | Description |
|--------|-------------|
| `widget` | Flutter widgets và usage |
| `package` | Packages với best practices |
| `pattern` | Design patterns và code snippets |
| `architect` | Architecture layers và dependencies |
| `chart` | Chart type recommendations |
| `color` | Color palettes theo product type |
| `typography` | Font pairings và styles |
| `style` | UI styles (Glassmorphism, etc.) |
| `ux` | UX guidelines |
| `icon` | Icon libraries và usage |
| `landing` | Landing page patterns |
| `naming` | Naming conventions |
| `product` | Product type recommendations |
| `prompt` | AI prompt templates |
| `performance` | Performance optimization patterns |
| `ui-reasoning` | UI decisions theo app category |
| `accessibility` | Mobile accessibility patterns |
| `motion` | Flutter animations & micro-interactions *(NEW)* |

### Example Prompts
- *"Thiết kế kiến trúc thư mục cho một ứng dụng eCommerce lớn theo Feature-First."*
- *"Tư vấn bảng màu và Typography cho một ứng dụng Fintech phong cách Dark Mode."*
- *"Review code snippet này theo tiêu chuẩn Dart 3 và Performance rules."*
- *"Tối ưu performance cho màn hình danh sách 1000+ items."*
- *"Hướng dẫn accessibility cho app Healthcare."*

---

## 🎯 Design System Generator & Dials (v2.5)

Tính năng flagship - tự động sinh **complete design system** cho Flutter app của bạn với bộ suy luận khép kín (Reasoning Contract) và các nút điều khiển trực quan.

### 🎛️ Design Dials (1-10)

Tùy chỉnh linh hoạt hệ thống thiết kế mà không cần viết prompt thủ công:

- `--variance <1-10>`: Biến thiên bố cục (`1-3`: Tối giản, đối xứng $\rightarrow$ `8-10`: Phá cách, Bento Grid, Expressive).
- `--motion <1-10>`: Cường độ hoạt họa (`1-3`: Subtle micro-interactions $\rightarrow$ `4-7`: Standard transitions/Hero $\rightarrow$ `8-10`: Complex physics).
- `--density <1-10>`: Mật độ bố cục (`1-3`: Thoáng đãng/Lifestyle $\rightarrow$ `4-7`: Chuẩn Material $\rightarrow$ `8-10`: Bảng điều khiển tài chính/Data tables).

### Commands

```bash
# 1. Generate với Design Dials
python3 src/flutter-pro-max/scripts/search.py "crypto trading wallet" --design-system --variance 8 --motion 5 --density 9 -p "CryptoPro"

# 2. Xuất trực tiếp mã nguồn Flutter ThemeData & ThemeExtension
python3 src/flutter-pro-max/scripts/search.py "e-commerce fashion" --design-system --export-dart -p "StyleShop"

# 3. Generate với Markdown output
python3 src/flutter-pro-max/scripts/search.py "e-commerce fashion" --design-system -f markdown -p "StyleShop"

# 4. Persist vào files (Master + Overrides pattern)
python3 src/flutter-pro-max/scripts/search.py "fintech banking" --design-system --persist -p "MyBank"

# 5. Tạo file override cho screen cụ thể
python3 src/flutter-pro-max/scripts/search.py "fintech banking" --design-system --persist -p "MyBank" --page "dashboard"
```

### Sample Output (ASCII Box with Dials & Motion)

```
+-----------------------------------------------------------------------------------------+
|  TARGET: CryptoPro - FLUTTER DESIGN SYSTEM                                              |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  DESIGN DIALS:                                                                          |
|     Variance: 8/10 (Bold / Expressive / Bento)                                          |
|     Motion:   5/10 (Standard)                                                           |
|     Density:  9/10 (Compact / High-Density Dashboard)                                   |
|                                                                                         |
|  SCREEN PATTERN: Hero + Features + CTA                                                  |
|     Sections: Hero > Features > CTA                                                     |
|     CTA: Bottom + Sticky                                                                |
|                                                                                         |
|  ARCHITECTURE: Clean Architecture + Feature-First                                       |
|     State: Riverpod / BLoC                                                              |
|                                                                                         |
|  UI STYLE: Typographic Brutalism                                                        |
|     Keywords: Giant text, sans-serif, black/white, minimal imagery, extreme weight      |
|                                                                                         |
|  COLOR PALETTE:                                                                         |
|     Primary:    #F59E0B                                                                 |
|     Secondary:  #FBBF24                                                                 |
|     CTA:        #8B5CF6                                                                 |
|     Background: #FFFFFF                                                                 |
|     Surface:    #F8FAFC                                                                 |
|     Text:       #1E293B                                                                 |
|                                                                                         |
|  MOTION INTELLIGENCE: Scroll Reveal (Standard)                                          |
|     Duration: 300-400ms | Curve: Curves.easeOutCubic                                    |
|     Snippet:  TweenAnimationBuilder<double>(tween: Tween(begin: 0.0, end: ...          |
|                                                                                         |
|  SPACING SCALE (VisualDensity.compact):                                                 |
|     xs: 2.0 | sm: 4.0 | md: 8.0 | lg: 12.0 | xl: 16.0                                  |
|                                                                                         |
|  PRE-DELIVERY CHECKLIST:                                                                |
|     [ ] const constructors used everywhere possible                                     |
|     [ ] Touch target >= 48x48 dp on mobile                                              |
|     [ ] Semantics widgets added for screen readers                                      |
|     [ ] MediaQuery.disableAnimationsOf respected                                        |
|     [ ] No God Widgets (files < 300 lines)                                              |
|                                                                                         |
+-----------------------------------------------------------------------------------------+
```

### Persist Design System (Master + Overrides Pattern)

Lưu design system vào files để **sử dụng nhất quán across sessions**:

```
design-system/
├── mybank/
│   ├── MASTER.md           # Global Source of Truth (colors, typography, spacing)
│   ├── app_theme.dart      # (Optional) Production Flutter Theme code
│   └── pages/
│       └── dashboard.md    # Screen-specific overrides
```

---

## 🔍 Flutter Design Review Subagent & Slash Command (NEW)

Không chỉ sinh code, **Flutter Pro Max** tích hợp subagent chuyên biệt để đánh giá, phản biện và rà soát giao diện người dùng theo 6 tiêu chuẩn khắt khe trước khi bàn giao:

```bash
# Sử dụng slash command
/flutter-review lib/features/dashboard/presentation/dashboard_screen.dart

# Hoặc kích hoạt subagent trong Claude Code / Antigravity
@flutter-design-review
```

### Quy Trình Audit 6 Pha:
1. **Layout Resilience**: Phát hiện nguy cơ tràn pixel (`RenderFlex overflowed`), thiếu flex constraint hoặc bàn phím che form.
2. **Touch Targets & Ergonomics**: Đảm bảo vùng bấm đạt chuẩn Material 3 ($\ge 48\times 48\text{ dp}$) và iOS HIG ($\ge 44\times 44\text{ pt}$).
3. **Accessibility & Font Scaling**: Rà soát nhãn `Semantics` và đảm bảo layout co giãn mượt mà khi người dùng bật `TextScaler` phóng to chữ 1.5x - 2.0x.
4. **Visual Polish & Tokens**: Triệt tiêu màu sắc hardcode (`Color(0xFF...)`), ép buộc sử dụng `Theme.of(context)` và Design Tokens đồng nhất.
5. **Motion & Haptics**: Kiểm tra curve chuyển động, giải phóng `AnimationController` trong `dispose()`, và tuân thủ `MediaQuery.disableAnimationsOf(context)`.
6. **Performance & Rebuild Hygiene**: Rà soát `const` constructors, giới hạn phạm vi rebuild (`Consumer`, `BlocBuilder`) và ngăn chặn `setState()` ở cấp root.

---

## 🛠️ Developer Utility Tools (NEW)

Flutter Pro Max tích hợp sẵn bộ công cụ tự động hóa chuẩn công nghiệp giúp bạn setup dự án nhanh chóng:

```bash
# 1. Sinh Makefile chuẩn hóa (build_runner, lint, format, test, coverage, flavors APK/IPA)
# 🎯 Tự động phát hiện FVM: Nếu project có .fvmrc, tự động dùng `fvm flutter`, ngược lại dùng SDK hệ thống!
npx flutter-pro-max makefile [-f]
make help

# 2. Sinh Fastlane CI/CD automation chuyên nghiệp cho Android & iOS
npx flutter-pro-max fastlane [-p android|ios|all] [-f]

# 3. Tự động thêm block loại trừ file nội bộ của skill & AI folders vào .gitignore
# Mặc định tự động quét và thêm đúng AI đang dùng trong project (.agents/, .claude/, .cursor/...)
npx flutter-pro-max gitignore

# Hoặc chỉ định rõ AI trợ lý cần ignore:
npx flutter-pro-max gitignore -a antigravity
npx flutter-pro-max gitignore -a claude
npx flutter-pro-max gitignore -a cursor

# Hoặc bảo vệ toàn diện trước toàn bộ 16 AI coding assistants:
npx flutter-pro-max gitignore --all
```

> 💡 **Tự động bảo vệ Git khi cài đặt:** Lệnh `flutter-pro-max init` mặc định sẽ tự động cập nhật `.gitignore` với các quy tắc phù hợp với chính AI bạn vừa chọn để ngăn rò rỉ assets (có thể bỏ qua bằng cờ `--skip-gitignore`).

---

## 📖 How It Works

1.  **Requirement Analysis**: AI phân tích yêu cầu, scale ứng dụng và tech stack bạn chọn (Riverpod, Bloc, etc.).
2.  **Domain Searching**: Tìm kiếm trong 18 kiến thức domain chuyên sâu (Architecture, UI, Performance, Accessibility, Motion).
3.  **Cross-Reference**: Đối chiếu với các pattern đã được thiết lập để đảm bảo không có xung đột giữa các thư viện.
4.  **Actionable Output**: Trả về hướng dẫn triển khai cụ thể, code snippets thực tế và các lưu ý (pro-tips).

---

## 📊 Data Files

| File | Records | Description |
|------|---------|-------------|
| widget.csv | 65 | Flutter widgets |
| package.csv | 100+ | Packages với alternatives |
| patterns.csv | 110 | Design patterns |
| architect.csv | 20+ | Architecture layers |
| flutter-performance.csv | 35 | Performance patterns |
| mobile-accessibility.csv | 35 | Accessibility patterns |
| ui-reasoning.csv | 35 | UI decision rules |
| colors.csv | 50+ | Color palettes |
| typography.csv | 40+ | Font pairings |
| styles.csv | 60+ | UI styles |
| ux-guidelines.csv | 50+ | UX rules |
| icons.csv | 100+ | Icon recommendations |
| landing.csv | 30+ | Landing patterns |
| products.csv | 40+ | Product recommendations |
| prompts.csv | 30+ | AI prompts |
| charts.csv | 20+ | Chart types |
| name_convention.csv | 10+ | Naming rules |

---

## 📄 License

Project này được cấp phép theo MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

## � Acknowledgements

Inspired by [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) by [@viettranx](https://github.com/viettranx). Kiến trúc, CLI design, và multi-platform skill system được adapt từ project tuyệt vời này.

---

## 📝 Changelog

Chi tiết toàn bộ lịch sử phát hành của các phiên bản được ghi nhận đầy đủ tại **[CHANGELOG.md](CHANGELOG.md)**.

### [v2.7.0] - 2026-09-10 (Latest)
- **🛡️ Production Hardening & Code Sentinel Audit Compliance**: Nâng cấp toàn diện 6 bộ quy tắc cốt lõi dựa trên thực tiễn quét mã nguồn dự án sản xuất (Code Sentinel SAST Audit):
  - **Guaranteed UI Cleanup (`05_error_handling.md`)**: Bắt buộc bọc mọi UI Loader / Dialog trong khối `finally` (`hideLoader()`), chống kẹt màn hình vĩnh viễn khi có ngoại lệ; cấm fake success; bắt buộc có UI Error State kèm nút Thử lại (Retry path) thay vì nuốt lỗi thành Empty State.
  - **Async Gap & Framework Lifecycle (`15_state_lifecycle.md`)**: Thiết lập rào chắn `if (!mounted) return;` trong StatefulWidget và `if (isClosed) return;` trong Controller (GetX/Bloc/Notifier). Chuẩn hóa vòng đời GetX (`onClose()`, cấm tự chế `dispose()`, hủy toàn bộ `Worker` debounce/ever). Cấm triệt để side-effects trong phương thức `build()`.
  - **Bảo mật File I/O & Network Hardening (`08_security.md`)**: Phòng vệ Path Traversal (`path.basename()` + regex sanitize), kiểm tra MIME type whitelist và kích thước file tối đa. Cấm bypass SSL trong WebView (`onReceivedServerTrustAuthRequest`), khóa domain allowlist và scheme https. Chuẩn hóa Log Masking (che token, password, Authorization header).
  - **Chống Re-entrancy & Search Race Condition (`03_interaction_flow.md`)**: Tự động vô hiệu hóa nút bấm khi đang xử lý async (`isSubmitting` guard), chống pop kép trên confirmation dialog. Chuẩn hóa tìm kiếm thời gian thực với debounce (300–500ms) kết hợp `CancelToken` hủy request cũ.
  - **Zero Force-Unwrap & Pure Build (`02_code_quality.md`)**: Cấm tuyệt đối toán tử ép null (`!`) trên Remote Data và dynamic json payload (thay bằng `firstOrNull`, `?.`, `?? fallback`); bắt buộc bảo đảm hàm `build()` thuần khiết (Pure Build Function, không in-place mutate).
  - **Localization SAST Hardening (`22_localization.md`)**: Quy ước tiền tố đặt tên key i18n (`lbl_`, `hint_`, `title_`, `msg_`) chống báo động giả hardcoded secrets trong công cụ quét SAST/CI-CD, kèm hướng dẫn exclude file từ điển.
- **🔄 Đồng bộ hóa 100% Assets**: Đồng bộ toàn bộ 22 rules giữa `src/flutter-pro-max/templates/base/rules/` và `cli/assets/templates/base/rules/`.

👉 Xem toàn bộ lịch sử các phiên bản trước tại **[CHANGELOG.md](CHANGELOG.md)**.

---

<div align="center">

**Built for developers, by experts. Happy coding!**

</div>
