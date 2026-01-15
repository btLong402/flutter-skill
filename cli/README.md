# Flutter Pro Max CLI

CLI để cài đặt Flutter Pro Max skill cho các AI coding assistants.

## Installation

### The Quick Way (Recommended)

```bash
npx flutter-pro-max-cli
```

### Global Installation

```bash
# Install globally
npm install -g flutter-pro-max-cli

# Initialize in any project
flutter-pro-max init
```

## Usage

### Interactive Mode

```bash
npx flutter-pro-max-cli
```

CLI sẽ tự động phát hiện AI assistants đã có và cho phép bạn chọn.

### Specific AI Assistant

```bash
npx flutter-pro-max-cli init --ai claude
npx flutter-pro-max-cli init --ai cursor
npx flutter-pro-max-cli init --ai all
```

### Available AI Types

| Type | Folder |
|------|--------|
| `claude` | `.claude/skills/` |
| `cursor` | `.cursor/commands/` |
| `windsurf` | `.windsurf/workflows/` |
| `antigravity` | `.agent/workflows/` |
| `copilot` | `.github/prompts/` |
| `kiro` | `.kiro/steering/` |
| `codex` | `.codex/skills/` |
| `roocode` | `.roo/commands/` |
| `qoder` | `.qoder/rules/` |
| `gemini` | `.gemini/skills/` |
| `codebuddy` | `.codebuddy/commands/` |
| `trae` | `.trae/skills/` |
| `all` | All of the above |

## After Installation

1. Install Python dependency:
   ```bash
   pip install rank-bm25
   ```

2. Restart your AI coding assistant

3. Try:
   ```
   Tạo màn hình đăng nhập với Riverpod
   ```

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Test locally
npm run dev
```

## License

MIT
