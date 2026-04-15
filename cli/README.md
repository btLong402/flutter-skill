# 🚀 Flutter Pro Max CLI

**The official command-line interface for deploying Flutter Pro Max technical intelligence to your favorite AI coding assistants.**

[![npm version](https://img.shields.io/npm/v/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Downloads](https://img.shields.io/npm/dm/flutter-pro-max-cli.svg)](https://www.npmjs.com/package/flutter-pro-max-cli)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📦 Installation

### The Quick Way (Recommended)
Bootstrap any project in seconds. This command will guide you through selecting and installing the skill for your environment.

```bash
npx flutter-pro-max-cli
```

### Global Installation
For heavy users who want the `flutter-pro-max` command available everywhere:

```bash
# Install globally
npm install -g flutter-pro-max-cli

# Initialize in your project
flutter-pro-max init
```

---

## 🛠️ Usage

### Interactive Setup
Simply run the command and follow the prompts to detect and install the skill for your active AI assistants.

```bash
flutter-pro-max init
```

### Scripted Installation
For CI/CD or automated setups, you can specify the assistant type directly:

```bash
# Install for a specific assistant
flutter-pro-max init --ai claude
flutter-pro-max init --ai cursor
flutter-pro-max init --ai antigravity

# Install for all supported assistants
flutter-pro-max init --ai all
```

### Other Commands

```bash
# List available versions from GitHub releases
flutter-pro-max versions

# Update to the latest version
flutter-pro-max update
flutter-pro-max update --ai claude
```

### npm Publish

The CLI can be published automatically from GitHub Actions via [.github/workflows/npm-publish.yml](../.github/workflows/npm-publish.yml).

Requirements:
- Add `NPM_TOKEN` to repository secrets
- Bump `cli/package.json` version before pushing to `main`
- The workflow skips publish if that exact version already exists on npm

---

## 🤖 Supported AI Assistants

This CLI bridges the gap between the Flutter Pro Max knowledge base and your development tools (16 platforms):

| Assistant | Type Flag | Install Type | Template | Limit |
|-----------|-----------|--------------|----------|-------|
| **Claude Code** | `claude` | Full | Full (~15KB) | No Limit |
| **Codex CLI** | `codex` | Full | Full (~15KB) | No Limit |
| **Continue** | `continue` | Full | Full (~15KB) | No Limit |
| **JetBrains AI (Junie)** | `junie` | Full | Full (~15KB) | No Limit |
| **Gemini CLI** | `gemini` | Full | Full (~15KB) | 1M+ Tokens |
| **OpenCode** | `opencode` | Full | Full (~15KB) | No Limit |
| **CodeBuddy** | `codebuddy` | Full | Full (~15KB) | No Limit |
| **Trae** | `trae` | Full | Full (~15KB) | No Limit |
| **Antigravity (Google)** | `antigravity` | Full | Compact (~5KB) | **12,000 chars** |
| **Cursor** | `cursor` | Reference | Full (~13KB) | No Limit |
| **Windsurf** | `windsurf` | Reference | Full (~13KB) | No Limit |
| **GitHub Copilot** | `copilot` | Full | Full (~15KB) | No Limit |
| **VS Code** | `vscode` | Full | Full (~15KB) | No Limit |
| **Kiro** | `kiro` | Reference | Full (~13KB) | No Limit |
| **RooCode** | `roocode` | Reference | Full (~13KB) | No Limit |
| **Qodo/Qoder** | `qoder` | Reference | Full (~13KB) | No Limit |

**Install Types:**
- **Full**: Data và scripts nằm trong skill folder (standalone, ~500KB)
- **Reference**: Skill file trỏ đến `.shared/` folder chung (tiết kiệm dung lượng khi dùng nhiều assistants)

**Templates (theo platform limits - dựa trên [Flutter AI Rules](https://docs.flutter.dev/ai/ai-rules)):**
- **Full (~15KB)**: Đầy đủ rules, code examples, Material 3 theming, accessibility
- **Compact (~5KB)**: Core rules, essential patterns (Antigravity 12k limit)
- **Mini (~2KB)**: Essential rules only (Copilot ~4k limit)

---

## 📊 What Gets Installed

### Rules Files (19 modules)
| Tier | Rules | Description |
|------|-------|-------------|
| **Foundation (5)** | 01-05 | Skill usage, Code quality, Interaction flow, Consistency, Error handling |
| **Code Quality (5)** | 06-10 | Testing, Performance, Security, State Management, Naming |
| **UX & Resilience (5)** | 11-15 | Accessibility, Network resilience, Offline-first, Graceful degradation, Lifecycle |
| **Product (4)** | 16-19 | Google Play ASO, Compliance, Visuals, Architecture decisions |

**Rules are automatically generated** into platform-specific locations:
- **Append mode** (Claude, Copilot): Rules concatenated into existing file
- **Create mode** (Cursor, Windsurf, others): Separate `.mdc` or `.md` files in rules folder

### Data Files (17 domains)
| Domain | File | Description |
|--------|------|-------------|
| Widgets | `widget.csv` | 65+ Flutter widgets |
| Packages | `package.csv` | 100+ packages với alternatives |
| Patterns | `patterns.csv` | 110+ design patterns |
| Architecture | `architect.csv` | Architecture layers |
| Performance | `flutter-performance.csv` | 35 optimization patterns |
| Accessibility | `mobile-accessibility.csv` | 35 accessibility patterns |
| UI Reasoning | `ui-reasoning.csv` | 35 app category decisions |
| Colors | `colors.csv` | 50+ color palettes |
| Typography | `typography.csv` | 40+ font pairings |
| Styles | `styles.csv` | 60+ UI styles |
| UX | `ux-guidelines.csv` | 50+ UX rules |
| Icons | `icons.csv` | 100+ icon recommendations |
| Landing | `landing.csv` | 30+ landing patterns |
| Products | `products.csv` | 40+ product recommendations |
| Prompts | `prompts.csv` | 30+ AI prompts |
| Charts | `charts.csv` | 20+ chart types |
| Naming | `name_convention.csv` | Naming conventions |

### Search Scripts
- `search.py` - BM25 search CLI
- `core.py` - Search engine core

---

## 🔧 Development

If you want to contribute or modify the CLI:

```bash
# Clone and install
git clone https://github.com/btLong402/flutter-skill.git
cd cli
npm install

# Build the project
npm run build

# Run locally
node dist/index.js init --ai claude

# Test search
node dist/index.js init --ai claude
cd .claude/skills/flutter-pro-max
python3 scripts/search.py "ListView" --domain widget --top 3
```

---

## 🔄 Syncing Assets (Rules & Data)

When you update rules or data files in the source directory, you must sync them to CLI assets before publishing.

### Sync Rules Only
After adding/updating rules in `src/flutter-pro-max/templates/base/rules/`:

```bash
# Copy all rules to CLI
cp -r src/flutter-pro-max/templates/base/rules/* cli/assets/templates/base/rules/

# Verify sync
ls cli/assets/templates/base/rules/ | wc -l  # Should show 19 files
```

### Sync All Assets (Complete)
Before publishing to npm:

```bash
# Sync data files (17 domains)
cp -r src/flutter-pro-max/data/* cli/assets/data/

# Sync scripts
cp -r src/flutter-pro-max/scripts/* cli/assets/scripts/

# Sync templates (skills + rules + platforms)
cp -r src/flutter-pro-max/templates/* cli/assets/templates/

# Verify
cd cli/assets
find . -type f | wc -l  # Should show significantly more files
```

### Pre-Publish Checklist
- [ ] All 19 rules present in `cli/assets/templates/base/rules/`
- [ ] All 17 data files present in `cli/assets/data/`
- [ ] All scripts present in `cli/assets/scripts/`
- [ ] Version bumped in `cli/package.json`
- [ ] No uncommitted changes in CLI files

> ⚠️ **CRITICAL:** Without syncing, users will not receive the latest rules/data when they run `flutter-pro-max-cli`

---

## 📁 Project Structure

```
cli/
├── src/
│   ├── index.ts              # CLI entry point
│   ├── commands/
│   │   ├── init.ts           # Install command
│   │   ├── versions.ts       # List versions
│   │   └── update.ts         # Update command
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   └── utils/
│       ├── detect.ts         # AI type detection
│       ├── github.ts         # GitHub API client
│       ├── logger.ts         # Console logger
│       └── template.ts       # Template renderer
├── assets/
│   ├── data/                 # 17 CSV knowledge files
│   ├── scripts/              # Python search scripts
│   └── templates/
│       ├── base/             # Markdown templates
│       │   ├── skill-content.md      # Full template (~13KB)
│       │   ├── skill-content-10k.md  # Compact (~5KB)
│       │   ├── skill-content-4k.md   # Mini (~2KB)
│       │   └── quick-reference.md    # Add-on (~2KB)
│       └── platforms/        # 16 platform JSON configs
├── package.json
└── tsconfig.json
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📝 Changelog

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

---

<div align="center">

**Streamline your Flutter development with AI-powered architectural intelligence.**

</div>
