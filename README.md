# Flutter Pro Max

> AI Skill cung cấp kiến thức chuyên sâu về Flutter, Clean Architecture, Performance và Modern Dart 3.

[![Flutter](https://img.shields.io/badge/Flutter-02569B?logo=flutter&logoColor=white)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart_3-0175C2?logo=dart&logoColor=white)](https://dart.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Flutter Pro Max là searchable database với **14 data sources**:

| Type | Content |
|------|---------|
| **Widget** | 65+ Flutter widgets với pro-tips |
| **Package** | 100+ packages với best practices |
| **Pattern** | 100+ design patterns với code snippets |
| **Architecture** | Clean Architecture layer paths |
| **Chart** | Chart type recommendations |
| **Color** | Color palettes by product type |
| **Typography** | Font pairings với Google Fonts |
| **Style** | UI style guidelines (Glassmorphism, Neubrutalism...) |
| **UX Guideline** | UX best practices (Do/Don't) |
| **Icon** | Icon recommendations |
| **Landing** | Landing page patterns |
| **Naming** | Dart/Flutter naming conventions |
| **Product** | Product type styling |
| **Prompt** | AI prompt templates |

## Installation

### The Quick Way (Recommended)

Bootstrap your project with the official CLI. It automatically detects your environment and installs the skill for your preferred AI assistants.

```bash
npx flutter-pro-max-cli
```

### Global Installation

For frequent use across multiple projects:

```bash
# Install globally
npm install -g flutter-pro-max-cli

# Initialize in any project
flutter-pro-max init
```

### Manual Installation

Copy các folders tương ứng vào project của bạn:

| AI Assistant | Folder cần copy |
|--------------|-----------------|
| Claude Code | `.claude/skills/flutter-pro-max/` |
| Cursor | `.cursor/commands/` |
| Windsurf | `.windsurf/workflows/` |
| Antigravity | `.agent/workflows/` |
| Gemini CLI | `.gemini/skills/flutter-pro-max/` |
| Codex | `.codex/skills/flutter-pro-max/` |
| GitHub Copilot | `.github/prompts/` |
| Kiro | `.kiro/steering/` |
| Trae | `.trae/skills/flutter-pro-max/` |
| Roo | `.roo/commands/` |
| Qoder | `.qoder/rules/` |
| CodeBuddy | `.codebuddy/commands/` |

**Lưu ý:** Cần copy thêm `.shared/` cho data và scripts.

## Prerequisites

```bash
# Chỉ cần Python (không cần pip install)
python3 --version
```

## Usage

### Claude Code

Skill tự động kích hoạt khi bạn yêu cầu Flutter work:

```
Tạo màn hình đăng nhập với Riverpod
```

### Cursor / Windsurf / Antigravity

Sử dụng slash command:

```
/flutter-pro-max Tạo màn hình đăng nhập với Riverpod
```

### Search Examples

```bash
# Auto-detect domain
python3 scripts/search.py "ListView pagination" --top 5

# Specific domain
python3 scripts/search.py "chart bar comparison" --domain chart --top 5

# Typography search
python3 scripts/search.py "font modern SaaS" --domain typography --top 5

# Color search
python3 scripts/search.py "fintech crypto dark" --domain color --top 5

# UX Guidelines
python3 scripts/search.py "touch target accessibility" --domain ux --top 5

# With stack filter (exclude conflicting packages)
python3 scripts/search.py "state management" --stack riverpod --top 5

# JSON output
python3 scripts/search.py "login" --json --top 3
```

## Features

### 1. Zero Dependencies BM25 Search
Self-contained BM25 search engine - không cần `pip install`.

### 2. Auto-detect Domain
Tự động phát hiện domain từ query keywords.

### 3. Widget Weight Boosting
Score x2 khi query khớp tên widget.

### 4. Package Category Filtering
Score x1.5 cho packages trong category phù hợp.

### 5. Stack Exclusion
Loại bỏ packages xung đột với stack đang dùng:
- `--stack riverpod`: Loại bỏ bloc, provider
- `--stack bloc`: Loại bỏ riverpod, provider
- `--stack provider`: Loại bỏ riverpod, bloc

## Technical Standards

Skill tuân thủ và đề xuất:

- **Dart 3**: Records, Pattern Matching, Sealed Classes
- **Sound Null Safety**: Không dùng `!` bừa bãi
- **Performance**: `const`, `SizedBox` > `Container`, `ListView.builder`
- **State Management**: Riverpod (default), Bloc (optional)
- **Architecture**: Clean Architecture with Feature-First
- **UX**: Touch targets 44x44px, WCAG contrast

## License

MIT License - See [LICENSE](LICENSE)

## Author

Built with ❤️ for Flutter developers
