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

# Install for all supported assistants
flutter-pro-max init --ai all
```

---

## 🤖 Supported AI Assistants

This CLI bridges the gap between the Flutter Pro Max knowledge base and your development tools:

| Assistant | Type Flag | Installation Path |
|-----------|-----------|-------------------|
| **Claude Code** | `claude` | `.claude/skills/` |
| **Cursor** | `cursor` | `.cursor/commands/` |
| **Windsurf** | `windsurf` | `.windsurf/workflows/` |
| **Antigravity** | `antigravity` | `.agent/workflows/` |
| **Trae** | `trae` | `.trae/skills/` |
| **Gemini CLI** | `gemini` | `.gemini/skills/` |
| **GitHub Copilot** | `copilot` | `.github/prompts/` |
| **RooCode** | `roocode` | `.roo/commands/` |
| **Kiro** | `kiro` | `.kiro/steering/` |
| **Qoder** | `qoder` | `.qoder/rules/` |
| **CodeBuddy** | `codebuddy` | `.codebuddy/commands/` |
| **Codex** | `codex` | `.codex/skills/` |

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

# Run locally in development mode
npm run dev
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Streamline your Flutter development with AI-powered architectural intelligence.**

</div>
