# 🚀 Flutter Pro Max CLI

**The official command-line interface for deploying Flutter Pro Max technical intelligence, modular rules, and developer automation tools to your favorite AI coding assistants.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD](https://github.com/btLong402/flutter-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/btLong402/flutter-skill/actions/workflows/ci.yml)

[Quick Start](#-quick-start) | [Commands](#-commands--usage) | [Supported Assistants](#-supported-ai-assistants) | [Architecture & Features](#-architecture--features) | [Changelog](#-changelog)

---

## ⚡ Quick Start

### One-liner Bootstrap (Recommended)
Cài đặt tức thì skill vào dự án của bạn mà không cần cài đặt global:

```bash
npx flutter-pro-max-cli
```

### Global Installation
Dành cho lập trình viên muốn sử dụng lệnh `flutter-pro-max` ở mọi nơi trên terminal:

```bash
# Cài đặt toàn cục
npm install -g flutter-pro-max-cli

# Khởi tạo trong dự án Flutter
flutter-pro-max init
```

---

## 🛠️ Commands & Usage

### 1. `flutter-pro-max init` (Khởi tạo Skill & Rules)

Cài đặt skill, bộ 22 Modular Rules và tự động bảo vệ `.gitignore`:

```bash
# Chế độ tương tác (tự động nhận diện trợ lý AI)
flutter-pro-max init

# Chỉ định cụ thể AI Assistant
flutter-pro-max init --ai claude
flutter-pro-max init --ai cursor
flutter-pro-max init --ai antigravity
flutter-pro-max init --ai windsurf
flutter-pro-max init --ai copilot

# Cài đặt đồng thời cho tất cả 16 AI trợ lý
flutter-pro-max init --ai all

# Ghi đè file cấu hình đã có
flutter-pro-max init -f

# Bỏ qua việc tự động cập nhật .gitignore
flutter-pro-max init --skip-gitignore
```

---

### 2. 🧰 Developer Utility Tools (Mới trong v2.5)

#### 📝 `flutter-pro-max makefile`
Sinh `Makefile` chuẩn hóa cho Flutter với **22 target** hỗ trợ toàn bộ vòng đời phát triển:
- **🎯 Tự động phát hiện FVM**: Nếu dự án có `.fvmrc` hoặc thư mục `.fvm/`, Makefile sẽ tự động điều phối `fvm flutter` và `fvm dart`; ngược lại sẽ fallback mượt mà về Flutter SDK hệ thống!
- **Code Generation & Watch**: `make build-runner`, `make watch`
- **Quality Assurance**: `make format` (line-length 120), `make lint` / `analyze`, `make test`, `make coverage` (HTML lcov report), `make check`
- **Build Flavors**: `make build-apk-dev`, `make build-apk-prod` (split-per-abi), `make build-appbundle-prod` (obfuscation + split-debug-info), `make build-ios-prod`

```bash
# Sinh Makefile vào thư mục gốc của dự án
flutter-pro-max makefile [-f]

# Xem danh sách target có màu sắc trực quan
make help
```

#### 🚀 `flutter-pro-max fastlane`
Khởi tạo cấu trúc CI/CD Fastlane chuyên nghiệp chuẩn cho cả Android và iOS:
- **Android**: `android/fastlane/Appfile` & `Fastfile` (lanes: `build_dev`, `build_prod`, `beta_firebase`, `deploy_internal`, `deploy_play_store`)
- **iOS**: `ios/fastlane/Appfile` & `Fastfile` (lanes: `certificates` via `match`, `build_dev`, `build_prod`, `beta_testflight`, `deploy_app_store`)
- **Bảo mật môi trường**: Tạo template `.env.fastlane.example` ở root dự án để quản lý keystore, bundle ID và tokens an toàn.

```bash
# Sinh Fastlane cho cả 2 nền tảng
flutter-pro-max fastlane [-f]

# Chỉ định cụ thể nền tảng
flutter-pro-max fastlane -p android
flutter-pro-max fastlane -p ios
```

#### 🛡️ `flutter-pro-max gitignore`
Tự động cấu hình `.gitignore` để ngăn chặn việc commit nhầm các assets nội bộ của skill (`.shared/`, `design-system/pages/`, `__pycache__/`, `*.pyc`, `.fvm/flutter_sdk`) và **thư mục sinh ra của từng trợ lý AI**:
- **Smart AI Detection**: Tự động phát hiện các thư mục AI đang có trong dự án (`.agents/`, `.claude/`, `.cursor/`, `.windsurf/`...) để thêm đúng phần cần thiết!
- **Tùy biến theo AI**: Chỉ định rõ AI cần cấu hình hoặc bỏ qua.
- **Tính Idempotent**: Chạy nhiều lần không bao giờ bị nhân đôi dòng.

```bash
# Tự động phát hiện AI trong dự án và cập nhật .gitignore
flutter-pro-max gitignore

# Chỉ định AI cụ thể:
flutter-pro-max gitignore -a antigravity  # Thêm .agents/
flutter-pro-max gitignore -a claude       # Thêm .claude/skills/flutter-pro-max/...
flutter-pro-max gitignore -a cursor       # Thêm .cursor/rules/, .shared/

# Thêm quy tắc bảo vệ trước toàn bộ 16 AI trợ lý:
flutter-pro-max gitignore --all
```

---

### 3. Các Lệnh Quản Lý Khác

```bash
# Xem danh sách phiên bản đã phát hành trên GitHub
flutter-pro-max versions

# Cập nhật skill lên phiên bản mới nhất
flutter-pro-max update
flutter-pro-max update --ai claude
```

---

## 🤖 Supported AI Assistants (16 Nền Tảng)

CLI liên kết cơ sở tri thức khổng lồ của Flutter Pro Max với môi trường AI của bạn:

| Assistant | Type Flag | Chế Độ Cài Đặt | Vị Trí Lưu Trữ | Giới Hạn Buffer |
|-----------|-----------|----------------|----------------|-----------------|
| **Claude Code** | `claude` | Full | `.claude/skills/` & `CLAUDE.md` | Không giới hạn |
| **Antigravity (Google)** | `antigravity` | Full | `.agents/skills/` & `.agents/rules/` | Tối ưu 12k chars |
| **Cursor** | `cursor` | Reference | `.cursor/rules/` (.mdc) & `.shared/` | Không giới hạn |
| **Windsurf** | `windsurf` | Reference | `.windsurf/rules/` & `.shared/` | Không giới hạn |
| **GitHub Copilot** | `copilot` | Full | `.github/skills/` & `.github/` | Không giới hạn |
| **VS Code** | `vscode` | Full | `.vscode/rules/` & `.github/skills/` | Không giới hạn |
| **Gemini CLI** | `gemini` | Full | `.gemini/skills/` & `.gemini/rules/` | 1M+ Tokens |
| **Trae** | `trae` | Full | `.trae/skills/` & `.trae/rules/` | Không giới hạn |
| **Roo Code** | `roocode` | Reference | `.roo/rules/` & `.shared/` | Không giới hạn |
| **Kiro** | `kiro` | Reference | `.kiro/rules/` & `.shared/` | Không giới hạn |
| **Continue** | `continue` | Full | `.continue/skills/` & `.continue/rules/` | Không giới hạn |
| **CodeBuddy** | `codebuddy` | Full | `.codebuddy/skills/` & `.codebuddy/rules/` | Không giới hạn |
| **Codex CLI** | `codex` | Full | `.codex/skills/` & `.codex/rules/` | Không giới hạn |
| **JetBrains AI (Junie)** | `junie` | Full | `.junie/skills/` & `.junie/rules/` | Không giới hạn |
| **OpenCode** | `opencode` | Full | `.opencode/skills/` & `.opencode/rules/` | Không giới hạn |
| **Qodo/Qoder** | `qoder` | Reference | `.qoder/rules/` & `.shared/` | Không giới hạn |

---

## 🧠 Architecture & Features (v2.5)

Sau khi cài đặt bằng CLI, dự án của bạn sẽ sở hữu các khả năng chuyên sâu:

```
src/flutter-pro-max/ (Source of Truth) -> Đồng bộ 100% vào cli/assets/
├── data/                            # 18 domain CSVs + Catalog Governance
├── scripts/
│   ├── search.py                    # BM25 Multi-domain Search CLI
│   ├── core.py                      # Search Engine lõi (18 domains)
│   ├── reasoning_contract.py        # Closed-Grammar Deterministic Rules Parser
│   ├── design_system.py             # Design Dials & Dart Code Generator
│   └── tests/                       # 21 unit tests bao phủ 100%
└── templates/
    ├── base/rules/                  # 20 Modular Rules (MDC / Markdown)
    └── tools/                       # Makefile, Fastlane, Gitignore templates
```

### 1. 🎛️ Design Dials & Dart Theme Generator
- **3 Cần gạt thiết kế (`--variance`, `--motion`, `--density`)**: Điều khiển biên độ sáng tạo layout, cường độ hoạt họa và mật độ spacing/VisualDensity từ 1 đến 10.
- **Xuất Dart Code Chuẩn (`--export-dart`)**: Tự động sinh `app_theme.dart` với Material 3 `ThemeData` và 3-Layer Tokens (`AppColors`, `AppSpacing`, `AppRadius`, `ThemeExtension<AppCustomTokens>`).

### 2. 🎬 Flutter Motion Intelligence (Domain #18)
Thư viện hoạt họa chuyên sâu `flutter-motion.csv` phân loại theo 3 tầng (Subtle, Standard, Complex), tích hợp sẵn code Flutter chuẩn (`TweenAnimationBuilder`, `Hero`, `PageRouteBuilder`, `Curves`) và chỉ dẫn tối ưu GPU/Accessibility (`MediaQuery.disableAnimationsOf`).

### 3. 🔍 Flutter Design Review Subagent & Command
Tích hợp subagent `@flutter-design-review` và slash command `/flutter-review` thực hiện audit 6 pha nghiêm ngặt:
1. **Layout Resilience** (chống lỗi `RenderFlex overflowed`)
2. **Touch Targets** ($\ge 48\times 48\text{ dp}$ Material 3 & $\ge 44\times 44\text{ pt}$ iOS HIG)
3. **Accessibility & Font Scaling** (`TextScaler` 1.5x - 2.0x, `Semantics`)
4. **Visual Polish & Tokens** (triệt tiêu hardcoded `Color(0xFF...)`)
5. **Motion & Haptics** (kiểm soát lifecycle `AnimationController`, disable animations)
6. **Performance & Rebuild Hygiene** (`const` widgets, giới hạn phạm vi rebuild)

---

## 📊 What Gets Installed

### 🧠 Rules Files (20 modules)
| Tier | Rules | Mô Tả |
|------|-------|-------|
| **Tier 1: Foundation (5)** | 01-05 | Tự động dùng skill, Code quality, Interaction flow (ABCR), App consistency, Error handling |
| **Tier 2: Code Quality (5)** | 06-10 | Testing (Unit/Widget), Performance (const/ListView), Security, State Management, Naming |
| **Tier 3: UX & Resilience (5)** | 11-15 | Accessibility, Network resiliency, Offline-first, Graceful degradation, State lifecycle |
| **Tier 4: Architecture & SDLC (5)** | 16-20 | Google Play ASO, Compliance, Visuals, Architecture Decision Matrix, Development Workflow |

### 📚 Data Files (18 domains)
Bao quát hơn **180+ thành phần kiến thức** được cấu trúc dạng CSV:
- `widget.csv` (65+ widgets), `package.csv` (100+ packages), `patterns.csv` (110+ patterns), `architect.csv` (layers & clean architecture)
- `flutter-performance.csv` (35 optimization rules), `mobile-accessibility.csv` (35 a11y patterns), `ui-reasoning.csv` (35 app categories)
- `flutter-motion.csv` (25+ animation presets), `colors.csv`, `typography.csv`, `styles.csv`, `ux-guidelines.csv`
- `icons.csv`, `landing.csv`, `products.csv`, `prompts.csv`, `charts.csv`, `name_convention.csv`

---

## 🔄 Assets Parity & Testing

CLI đảm bảo tính toàn vẹn tuyệt đối thông qua bộ test suite chạy song song trong CI/CD:

```bash
# Chạy toàn bộ test suites kiểm tra dữ liệu và CLI tools
python3 -m unittest discover -s src/flutter-pro-max/scripts/tests/
python3 -m unittest discover -s cli/assets/scripts/tests/
```

- **Data Integrity**: Đảm bảo 18 file CSV có đầy đủ schema và dữ liệu.
- **Assets Parity Guard**: Kiểm tra so sánh byte-level giữa `src/` và `cli/assets/` để ngăn ngừa drift trước khi release.
- **E2E CLI Testing**: Kiểm thử tự động quá trình sinh Makefile, Fastlane, Gitignore và chạy search từ skill vừa cài.

---

## 📁 Project Structure

```
cli/
├── src/
│   ├── index.ts              # CLI entry point & command registration
│   ├── commands/
│   │   ├── init.ts           # Cài đặt skill & tự động cập nhật .gitignore
│   │   ├── tools.ts          # Bộ sinh Makefile, Fastlane, Gitignore theo AI
│   │   ├── versions.ts       # Danh sách release versions
│   │   └── update.ts         # Cập nhật skill
│   ├── types/
│   │   └── index.ts          # TypeScript interfaces & AITypes
│   └── utils/
│       ├── detect.ts         # Tự động phát hiện AI trong thư mục dự án
│       ├── template.ts       # Template rendering engine
│       └── logger.ts         # Terminal color logger
├── assets/                   # Bản sao canonical đồng bộ 100% từ src/
│   ├── data/                 # 18 CSV datasets + metadata governance
│   ├── scripts/              # Python search engine & design system generator
│   └── templates/
│       ├── base/             # Base skill markdown templates & 22 rules
│       ├── tools/            # Makefile.template, Fastlane, Gitignore
│       └── platforms/        # 16 platform JSON configuration files
├── package.json
└── tsconfig.json
```

---

## 📝 Changelog

### v2.6.0 (2026-09-07)
- **🧠 22 Modular Rules (Tier 5 Expansion)**: Mở rộng hệ thống lên 22 rules với Tier 5:
  - `21_navigation_governance.md`: Chuẩn hóa Declarative Routing (`go_router`), type-safe parameters, Auth Redirect Guards và kiểm tra Deep Link an toàn.
  - `22_localization.md`: Thiết lập tiêu chuẩn cấm hardcode chuỗi text trên UI (**Zero Hardcoded Strings**), chuẩn hóa định dạng ARB và extension `context.l10n`.
- **🛡️ Ironclad Compliance Framework (Ép buộc AI tuân thủ Rules)**:
  - **Pre-Flight Compliance Block**: Bắt buộc AI phải xuất khối YAML cam kết thẩm định tiêu chuẩn kiến trúc và hard constraints trước khi sinh bất kỳ dòng code Dart nào.
  - **Ngưỡng hành động mềm 200 dòng**: Bắt buộc chủ động phân rã file khi ước tính đạt $\ge 200$ dòng thay vì chờ chạm trần 300 dòng.
- **✨ 100% Vietnamese Diacritics Standardization**: Chuẩn hóa toàn bộ 22 rules sang tiếng Việt có dấu đầy đủ, tối ưu hóa quá trình phân giải token của BPE Tokenizer, ngăn ngừa hallucination và hiểu sai chỉ thị.
- **⚡ Context Window Token Optimization**: Tinh chỉnh cấu hình `globs` cho nhóm Rule Google Play Store (`16`, `17`, `18`) giúp tiết kiệm ~1,000 tokens cho mỗi lượt prompt lập trình thông thường.
- **🛠️ Production Reference Implementations**: Bổ sung code mẫu thực chiến của `ResilientRetryInterceptor` (Dio Backoff + Jitter trong Rule 12), Stream Repository (Offline-first trong Rule 13) và checklist `dispose()` (Rule 15).

### v2.5.1 (2026-09-07)
- **🛡️ AI-Tailored Gitignore**: Hỗ trợ may đo quy tắc `.gitignore` riêng biệt cho 16 nền tảng trợ lý AI (`-a <type>`, `--all`). Tự động phát hiện AI đang sử dụng và chèn chính xác các thư mục như `.agents/`, `.claude/skills/`, `.cursor/rules/`, `.shared/`, v.v.
- **🎯 FVM Auto-Detection in Makefile**: Makefile template tự động kiểm tra sự tồn tại của `.fvmrc` hoặc `.fvm/` để tự điều phối giữa `fvm flutter` / `fvm dart` và Flutter SDK hệ thống.
- **🔄 Unified CI/CD Pipeline**: Đồng bộ hóa CI/CD, kiểm thử 21 unit tests, assets parity và CLI E2E tests trước khi publish lên npm registry.
- **📜 Restored Full Changelog**: Khôi phục và chuẩn hóa toàn bộ lịch sử thay đổi từ v2.0.0 đến v2.5.1.

### v2.5.0 (2026-09-07)
- **🧰 Developer Utility Tools**: Bổ sung bộ 3 công cụ tự động hóa `makefile` (kèm auto-detect FVM), `fastlane` (CI/CD Android & iOS) và `gitignore` (may đo riêng cho từng AI trợ lý).
- **🛡️ AI-specific Gitignore**: Tự động nhận diện trợ lý AI (`antigravity`, `claude`, `cursor`, `copilot`...) để ngăn ngừa rò rỉ file skill/rules lên repository.
- **🎛️ Design Dials**: 3 nút điều khiển `--variance`, `--motion`, `--density` tinh chỉnh biên độ sáng tạo, hoạt họa và spacing.
- **🐦 Production Dart Theme Generator**: Tùy chọn `--export-dart` xuất trực tiếp `app_theme.dart` chuẩn Material 3 với 3-Layer Tokens.
- **🎬 Flutter Motion Intelligence**: Bổ sung domain thứ 18 `motion` với cơ sở dữ liệu `flutter-motion.csv`.
- **🛡️ Closed-Grammar Reasoning Contract**: Tích hợp `reasoning_contract.py` loại bỏ hoàn toàn AI hallucination.
- **🔍 Flutter Design Review Subagent & Command**: Ra mắt subagent `@flutter-design-review` và slash command `/flutter-review` với quy trình audit 6 pha.
- **📊 20 Modular Rules**: Cập nhật chuẩn hóa đủ 20 rules với [20_development_workflow.md](file:///Users/longbt/Documents/dev/private/flutter-skill/src/flutter-pro-max/templates/base/rules/20_development_workflow.md).
- **🔄 Unified CI/CD Pipeline**: Tích hợp luồng test 21 unit tests (Python 3.10-3.12), test E2E CLI và tự động publish lên npm registry khi xanh 100%.

### v2.4.5 (2026-05-14)
- **📋 Development Workflow Rule**: Bổ sung rule 20 chuẩn hóa quy trình SDLC 8 bước.
- **🏗️ Architecture Decision Matrix**: Tích hợp hướng dẫn kiến trúc Greenfield vs Brownfield.

### v2.3.0 (2026-02-06)
- **VS Code 1.109 Support**: GitHub Copilot và VS Code sử dụng `.github/skills/` format
- **Breaking Change**: Copilot/VS Code chuyển từ prompts/instructions sang Skills
- **Full Install**: Copilot và VS Code nay sử dụng full template (~15KB) thay vì mini

### v2.2.0 (2026-02-02)
- **Flutter AI Rules**: Cập nhật theo [Flutter Official AI Rules](https://docs.flutter.dev/ai/ai-rules)
- **Platform Limits**: Tạo templates phù hợp với giới hạn từng platform
  - `skill-content.md` (~13KB) - Full template
  - `skill-content-10k.md` (~5KB) - Compact (Antigravity)
  - `skill-content-4k.md` (~2KB) - Mini (Copilot, VS Code)
- **New Platforms**: JetBrains AI (Junie), VS Code
- **Native-First State**: ValueNotifier/ChangeNotifier mặc định

### v2.1.0 (2026-01-27)
- **Type Safety**: Full Python type hints cho Pylance strict mode
- **Python 3.10+**: Minimum Python version updated
- **Code Quality**: Xóa unused imports, fix linter warnings

### v2.0.0
- Phiên bản đầu tiên với 14 AI assistant support
- BM25-based semantic search engine
- Design System Generator

---

## 📄 License

Project này được cấp phép theo [MIT License](LICENSE).
