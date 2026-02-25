# ⚡ Flutter Pro Max

**Expert architectural intelligence for building high-performance, scalable, and modern Flutter applications.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Flutter](https://img.shields.io/badge/Flutter-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart_3-0175C2?logo=dart&logoColor=white)](https://dart.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

[Overview](#-overview) | [Features](#-features) | [Installation](#-installation) | [Usage](#-usage) | [Supported Assistants](#-supported-ai-assistants)

---

## 🌟 Overview

**Flutter Pro Max** là một lớp AI Intelligence chuyên sâu dành cho phát triển Flutter hiện đại, được xây dựng dựa trên [Flutter AI Rules](https://docs.flutter.dev/ai/ai-rules) chính thức. Nó cung cấp cho các AI coding assistant một cơ sở kiến thức khổng lồ về các kiến trúc (Clean Architecture, Feature-First), Native-First state management (ValueNotifier, ChangeNotifier), tối ưu hóa hiệu năng, tiêu chuẩn bảo mật và các patterns thiết kế UI/UX cao cấp.

Dù bạn đang xây dựng một ứng dụng Fintech phức tạp, một sàn thương mại điện tử quy mô lớn hay một SaaS Dashboard, skill này đảm bảo AI partner của bạn sẽ đưa ra các khuyến nghị cấp độ chuyên gia dựa trên các tiêu chuẩn công nghiệp mới nhất.

---

## 🧠 Architecture: Rules (Brain) + Skill (Hands)

Flutter Pro Max tách biệt hoàn toàn **logic ra quyết định** và **công cụ thực thi**:

| Layer | Vai trò | Nội dung |
|-------|---------|----------|
| **🧠 Rules (Brain)** | System prompt, persona, constraints | 11 modular rule files — định nghĩa cách suy nghĩ, giới hạn an toàn, luồng quyết định |
| **🤲 Skill (Hands)** | Tools, search, data access | Search commands, 17 domain data files, design system generator |

### 🧠 11 Modular Rules

```
rules/
├── 01_skill_usage          # Tự động search skill trước khi code
├── 02_code_quality         # Think-before-code, God file prevention
├── 03_interaction_flow     # ABCR workflow
├── 04_app_consistency      # Design tokens, widget patterns
├── 05_error_handling       # Try-catch patterns, logging
├── 06_testing              # Test requirements, Arrange-Act-Assert
├── 07_performance          # const, ListView.builder, isolates
├── 08_security             # API keys, auth, data protection
├── 09_state_management     # Native-first hierarchy
├── 10_naming_conventions   # File/class naming, git commits
└── 11_accessibility        # Semantics, contrast, touch targets
```

Rules được gen **modular** — mỗi file tách biệt theo concern, chỉ kích hoạt khi cần, tránh loãng context window.

> 📖 **Reference:** [Flutter AI Rules](https://docs.flutter.dev/ai/ai-rules)

---

## 🚀 Features

Hệ thống kiến thức được xây dựng trên dữ liệu có cấu trúc bao quát hơn **150+ thành phần**:

- **� Intelligent Design System Generator** *(NEW)*: Tự động sinh complete design system (colors, typography, spacing, patterns) dựa trên app category với reasoning engine.
- **�🏗️ Architecture Excellence**: Clean Architecture, Feature-First, DDD, Repository Pattern, và Modular Design.
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
| **Antigravity** | Full | `.agent/skills/flutter-pro-max/` | `.agent/rules/` |
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

## 🛠️ Usage

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

# Tìm kiếm theo stack (loại bỏ packages xung đột)
python3 src/flutter-pro-max/scripts/search.py "state management" --stack riverpod --top 5
```

### Available Search Domains (17 total)

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

### Example Prompts
- *"Thiết kế kiến trúc thư mục cho một ứng dụng eCommerce lớn theo Feature-First."*
- *"Tư vấn bảng màu và Typography cho một ứng dụng Fintech phong cách Dark Mode."*
- *"Review code snippet này theo tiêu chuẩn Dart 3 và Performance rules."*
- *"Tối ưu performance cho màn hình danh sách 1000+ items."*
- *"Hướng dẫn accessibility cho app Healthcare."*

---

## 🎯 Design System Generator (NEW)

Tính năng flagship - tự động sinh **complete design system** cho Flutter app của bạn.

### Generate Design System

```bash
# Generate design system với ASCII output
python3 src/flutter-pro-max/scripts/search.py "fintech banking app" --design-system -p "MyBank"

# Generate với Markdown output
python3 src/flutter-pro-max/scripts/search.py "e-commerce fashion" --design-system -f markdown -p "StyleShop"
```

### Sample Output

```
+-----------------------------------------------------------------------------------------+
|  TARGET: MYBANK - FLUTTER DESIGN SYSTEM                                                 |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|  ARCHITECTURE: Clean Architecture + Security-First                                      |
|     Structure: Feature-First / Clean Architecture                                       |
|     State: Riverpod                                                                     |
|     Patterns: Secure Form Pattern, Biometric Auth, Transaction List                     |
|                                                                                         |
|  UI STYLE: Minimalism & Swiss Style                                                     |
|     Keywords: Clean, professional, trustworthy, secure                                  |
|     Best For: Banking, fintech, enterprise apps                                         |
|                                                                                         |
|  COLOR PALETTE:                                                                         |
|     Primary:    #1E3A5F (Deep Navy)                                                     |
|     Secondary:  #2563EB (Trust Blue)                                                    |
|     CTA:        #10B981 (Success Green)                                                 |
|     Background: #FFFFFF                                                                 |
|     Surface:    #F8FAFC                                                                 |
|     Text:       #1E293B                                                                 |
|                                                                                         |
|  TYPOGRAPHY: Inter / Inter                                                              |
|     Mood: Professional, clean, readable                                                 |
|                                                                                         |
|  AVOID (Anti-patterns):                                                                 |
|     Bright neon colors + Playful animations + Casual fonts + AI purple gradients        |
|                                                                                         |
|  PRE-DELIVERY CHECKLIST:                                                                |
|     [ ] const constructors for immutable widgets                                        |
|     [ ] Accessibility: Semantics labels, touch targets >= 48px                          |
|     [ ] Performance: ListView.builder for long lists                                    |
+-----------------------------------------------------------------------------------------+
```

### Persist Design System (Master + Overrides Pattern)

Lưu design system vào files để **sử dụng nhất quán across sessions**:

```bash
# Generate và persist vào design-system/mybank/MASTER.md
python3 src/flutter-pro-max/scripts/search.py "fintech banking" --design-system --persist -p "MyBank"

# Tạo thêm file override cho screen cụ thể
python3 src/flutter-pro-max/scripts/search.py "fintech banking" --design-system --persist -p "MyBank" --page "dashboard"
```

Tạo cấu trúc `design-system/`:

```
design-system/
├── mybank/
│   ├── MASTER.md           # Global Source of Truth (colors, typography, spacing)
│   └── pages/
│       └── dashboard.md    # Screen-specific overrides
```

**Cách sử dụng hierarchical retrieval:**
1. Khi build một screen (e.g., "Checkout"), kiểm tra `design-system/mybank/pages/checkout.md` trước
2. Nếu file tồn tại, rules trong đó **override** MASTER.md
3. Nếu không, sử dụng `design-system/mybank/MASTER.md`

---

## 📖 How It Works

1.  **Requirement Analysis**: AI phân tích yêu cầu, scale ứng dụng và tech stack bạn chọn (Riverpod, Bloc, etc.).
2.  **Domain Searching**: Tìm kiếm trong 17 kiến thức domain chuyên sâu (Architecture, UI, Performance, Accessibility).
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

### v2.3.2 (2026-02-25)
- **🧠 Rules/Skill Separation**: Tách hoàn toàn Brain (Rules) và Hands (Skill)
- **📦 11 Modular Rules**: Skill usage, Code quality, ABCR, Consistency, Error handling, Testing, Performance, Security, State management, Naming, Accessibility
- **🤲 Skill Tools-Only**: Skill content chỉ còn search commands + data reference (giảm 447 → 105 dòng)
- **📂 Modular Generation**: Platforms create-mode gen 11 files riêng, append-mode gộp vào 1 file

### v2.3.1 (2026-02-25)
- **🤖 Standalone Rules Generation**: CLI tự động gen rules file riêng biệt khỏi skill
- **📁 Source of Truth**: Restructure `src/flutter-pro-max/` làm canonical source
- **🧹 Cleanup**: Xóa files thừa, giảm từ 118 → 99 tracked files
- **🆕 3 New Domains**: `performance`, `accessibility`, `ui-reasoning`
- **🔧 CLI Enhancements**: Thêm `extract.ts`, `.gitignore`, `.npmignore`
- **16 Platforms**: Tất cả platforms đều hỗ trợ rules file generation

### v2.2.0 (2026-02-02)
- **Flutter AI Rules**: Cập nhật theo [Flutter Official AI Rules](https://docs.flutter.dev/ai/ai-rules)
- **Native-First State Management**: Mặc định ValueNotifier/ChangeNotifier thay vì Riverpod
- **Platform Limits**: Tạo templates phù hợp với giới hạn từng platform (4k, 10k, full)
- **New Platforms**: Thêm JetBrains AI (Junie), VS Code
- **AI Tools Integration**: Thêm dart_format, dart_fix, analyze_files guidelines
- **Material 3 Theming**: ThemeExtension, ColorScheme.fromSeed
- **Documentation**: Dart 3 patterns, accessibility, testing standards

### v2.1.0 (2026-01-27)
- **Type Safety**: Full Python type hints cho Pylance strict mode compatibility
- **Python 3.10+**: Cập nhật minimum Python version (sử dụng modern union syntax `str | None`)
- **Code Quality**: Xóa unused imports, fix tất cả linter warnings

### v2.0.0
- Phiên bản public đầu tiên với 14 AI assistant support
- BM25-based semantic search engine
- Design System Generator

---

<div align="center">

**Built for developers, by experts. Happy coding!**

</div>
