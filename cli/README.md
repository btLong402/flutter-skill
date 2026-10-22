# 🚀 Flutter Pro Max CLI

**The official command-line interface for deploying Flutter Pro Max technical intelligence, modular rules, and developer automation tools to your favorite AI coding assistants.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/btLong402/flutter-skill/blob/main/LICENSE)
[![CI/CD](https://github.com/btLong402/flutter-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/btLong402/flutter-skill/actions/workflows/ci.yml)

[Quick Start](#-quick-start) | [Commands](#-commands--usage) | [Supported Assistants](#-supported-ai-assistants) | [Architecture & Features](#-architecture--features) | [Changelog](https://github.com/btLong402/flutter-skill/blob/main/CHANGELOG.md)

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

Cài đặt bộ đôi skill (Flutter Code Intelligence & Mobile-Tablet UI/UX Audit), bộ 23 Modular Rules và tự động bảo vệ `.gitignore`:

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
│   ├── skills/               # mobile-tablet-ux-audit skill package
│   ├── templates/
│   │   ├── base/             # Base skill markdown templates & 23 rules
│   │   ├── tools/            # Makefile.template, Fastlane, Gitignore
│   │   └── platforms/        # 16 platform JSON configuration files
├── package.json
└── tsconfig.json
```

---

## 🔒 Privacy & Anonymous Telemetry

CLI và các scripts đi kèm tích hợp cơ chế thu thập phản hồi ẩn danh nhằm cải thiện độ phủ dữ liệu:
- **Nguyên tắc:** Chỉ gửi khi tra cứu bị thiếu (`count == 0`), kết quả gượng ép (`weak_match`), hoặc phát hiện tiêu chí audit lạ.
- **Bảo mật:** Không bao giờ đọc code dự án; tự động ẩn danh hóa và cắt lọc đường dẫn file cục bộ (`[PATH]`), email (`[EMAIL]`), Auth token/secrets (`[SECRET]`), và địa chỉ IP (`[IP]`).
- **Tắt dễ dàng (Opt-Out):**
  ```bash
  export DO_NOT_TRACK=1
  # hoặc:
  export FLUTTER_PRO_MAX_TELEMETRY=0
  ```

---

## 📝 Changelog

Chi tiết toàn bộ lịch sử phát hành của các phiên bản được ghi nhận đầy đủ tại **[CHANGELOG.md](https://github.com/btLong402/flutter-skill/blob/main/CHANGELOG.md)**.

### [v2.10.0] - 2026-10-22 (Latest)
- **🎨 Nâng Cấp Rubric v2 Cho Mobile & Tablet UX Audit (`mobile-tablet-ux-audit`)**: Mở rộng từ 10 lên **12 tiêu chí đánh giá định lượng** (tổng trọng số 100), bổ sung `performance_perceived` (Hiệu năng cảm nhận & độ mượt, trọng số 5) và `theming_dark_mode` (Theming & Dark mode, trọng số 4).
- **🔄 Tương thích ngược 100% với Scorecard v1 (10 tiêu chí)**: Tự động phát hiện phiên bản và áp dụng đúng bảng trọng số. Tự động quy đổi tên gọi khác (`ALIASES`) về khóa chuẩn của rubric.
- **📝 Đề xuất khoảng trống Rubric (`rubric_gaps`)**: Cho phép ghi nhận các khía cạnh chuyên biệt vào scorecard mà không làm sai lệch điểm số chuẩn, tự động tổng hợp trong báo cáo Markdown & JSON.
- **🛡️ Cập nhật Rule 23, Rule 01, Rule 20 và CLI Templates**: Đồng bộ quy chuẩn đánh giá 12 tiêu chí trên toàn bộ 16 AI coding assistants.
- **🧪 Mở rộng Test Suite**: Bổ sung unit tests cho Rubric v2, kiểm tra chuẩn xác toàn bộ test suite đạt 100% asset parity.

### [v2.9.0] - 2026-10-16
- **📡 Telemetry & Knowledge Gap Feedback Loop**: Tự động phát hiện thiếu hụt tri thức và tiêu chí đánh giá khi người dùng hoặc AI tra cứu không thấy kết quả (`count == 0`), độ khớp BM25 gượng ép (`token_coverage < 0.35` hoặc điểm thấp), xung đột công nghệ (stack incompatibility), hoặc tiêu chí UI/UX chưa có.
- **🔒 Privacy-First Data Sanitization**: Cơ chế làm sạch dữ liệu tự động cực kỳ nghiêm ngặt: loại bỏ đường dẫn file local, email, token bảo mật/API key, IP; cắt ngắn tối đa 200 ký tự. Tôn trọng tuyệt đối cờ `DO_NOT_TRACK=1` và `FLUTTER_PRO_MAX_TELEMETRY=0`.
- **☁️ Cloudflare Worker & D1 SQL Storage**: Hạ tầng serverless zero-cost với Cloudflare D1 lưu trữ lên tới 5 GB (100k lượt ghi/ngày), tổng hợp gộp `hit_count` (UPSERT) chống trùng lặp, bảo vệ chống spam (Rate limit 30 req/phút/IP), tích hợp Webhook Discord/Telegram và Web Dashboard theo dõi trực quan.
- **⚡ Async Non-Blocking Daemon**: Dispatch bất đồng bộ hoàn toàn trong luồng ngầm daemon với thời gian timeout ngắn (1.5s) và cơ chế `atexit` graceful flush (1.0s), không gây chậm hay gián đoạn quá trình làm việc của lập trình viên.
- **🚩 Cờ `--report-gap` (`-rg`)**: Cho phép người dùng và AI chủ động gửi góp ý về tri thức còn thiếu hoặc tiêu chí audit cần bổ sung trực tiếp từ terminal.

### [v2.8.0] - 2026-10-15
- **🎨 Tích hợp Skill mới: Mobile & Tablet UI/UX Audit (`mobile-tablet-ux-audit`)**: Đóng gói bộ công cụ audit UI/UX chuyên sâu vào CLI: `score.py` (chấm điểm định lượng 10 tiêu chí mobile+tablet, hard caps, backlog ưu tiên), `contrast.py` (đo độ tương phản WCAG 2.x, gợi ý màu), rubric checklist, và 41 automated unit tests.
- **🧠 23 Modular Rules (Rule 23: UI/UX Audit & Quality Governance)**: Quy chuẩn hóa kiểm thử giao diện định lượng, bằng chứng thực chứng, layout thích ứng tablet $\ge 600\text{dp}$ với NavigationRail & List-Detail.
- **⚡ Context-Aware Skill Usage & Fast-Path Routing (Rule 01)**: Phân luồng thông minh: Full-Flight cho tính năng mới/kiến trúc/audit, Fast-Path đi tắt cho hotfix nhỏ (< 15 dòng)/typo/config.
- **🔄 SDLC 8 bước tích hợp UI/UX Audit (Rule 20)**: Gắn kết bước kiểm thử UI/UX định lượng vào Step 3 và Step 7.
- **🚀 CLI Dual-Skill Auto-Installer**: Lệnh `flutter-pro-max init` tự động cài đặt song song cả 2 skills (`flutter-pro-max` + `mobile-tablet-ux-audit`) và 23 rules cho toàn bộ 16 trợ lý AI.
- **🧪 Mở rộng Test Suite lên 85 tests**: Đạt tỷ lệ vượt qua 100% trên toàn bộ các bộ kiểm thử tự động.

### [v2.7.0] - 2026-09-10
- **🛡️ Production Hardening & Code Sentinel Audit Compliance**: Nâng cấp toàn diện 6 bộ quy tắc cốt lõi dựa trên thực tiễn quét mã nguồn dự án sản xuất (Code Sentinel SAST Audit).

👉 Xem toàn bộ lịch sử các phiên bản trước tại **[CHANGELOG.md](https://github.com/btLong402/flutter-skill/blob/main/CHANGELOG.md)**.

---

## 📄 License

Project này được cấp phép theo [MIT License](https://github.com/btLong402/flutter-skill/blob/main/LICENSE).
