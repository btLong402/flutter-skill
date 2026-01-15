#!/bin/bash

# Sync scripts from root/scripts to all hidden tool folders
# This ensures that AI tool folders always have the latest core.py and search.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_DIR="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$(dirname "$CLI_DIR")"
SRC_SCRIPTS_DIR="$ROOT_DIR/scripts"

echo "🔄 Syncing core scripts to AI tool directories..."

# List of target script directories in hidden folders
TOOL_SCRIPT_DIRS=(
  ".agent/workflows/scripts"
  ".claude/skills/flutter-pro-max/scripts"
  ".cursor/commands/scripts"
  ".gemini/skills/flutter-pro-max/scripts"
  ".trae/skills/flutter-pro-max/scripts"
  ".windsurf/workflows/scripts"
  ".qoder/rules/scripts"
  ".roo/commands/scripts"
  ".codex/skills/flutter-pro-max/scripts"
  ".github/prompts/scripts"
  ".kiro/steering/scripts"
  ".codebuddy/commands/scripts"
)

# Core files to sync
CORE_FILES=("core.py" "search.py")

for tool_dir in "${TOOL_SCRIPT_DIRS[@]}"; do
  TARGET_PATH="$ROOT_DIR/$tool_dir"
  if [ -d "$TARGET_PATH" ]; then
    echo "  📁 Syncing to $tool_dir..."
    for file in "${CORE_FILES[@]}"; do
      if [ -f "$SRC_SCRIPTS_DIR/$file" ]; then
        cp "$SRC_SCRIPTS_DIR/$file" "$TARGET_PATH/"
      fi
    done
  else
    echo "  ⚠️ Warning: $tool_dir not found, skipping script sync."
  fi
done

echo "✅ Script synchronization complete!"
