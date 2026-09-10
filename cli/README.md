# 🚀 Flutter Pro Max CLI

**The official command-line interface for deploying Flutter Pro Max technical intelligence, modular rules, and developer automation tools to your favorite AI coding assistants.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI/CD](https://github.com/btLong402/flutter-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/btLong402/flutter-skill/actions/workflows/ci.yml)

[Quick Start](#-quick-start) | [Commands](#-commands--usage) | [Supported Assistants](#-supported-ai-assistants) | [Architecture & Features](#-architecture--features) | [Changelog](CHANGELOG.md)

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

## 📄 License

Project này được cấp phép theo [MIT License](LICENSE).
