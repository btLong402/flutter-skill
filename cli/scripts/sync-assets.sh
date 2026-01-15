#!/bin/bash

# Sync source files from root to cli/assets
# This ensures assets are always up-to-date before publishing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_DIR="$(dirname "$SCRIPT_DIR")"
ROOT_DIR="$(dirname "$CLI_DIR")"
ASSETS_DIR="$CLI_DIR/assets"

echo "🔄 Syncing assets from root to cli/assets..."

# First, sync scripts to hidden tool folders
bash "$SCRIPT_DIR/sync-tool-scripts.sh"

# List of directories to sync
DIRS=(
    ".agent"
    ".claude"
    ".codebuddy"
    ".codex"
    ".cursor"
    ".gemini"
    ".github"
    ".kiro"
    ".qoder"
    ".roo"
    ".shared"
    ".trae"
    ".windsurf"
)

# Remove old assets and recreate
rm -rf "$ASSETS_DIR"
mkdir -p "$ASSETS_DIR"

# Copy each directory
for dir in "${DIRS[@]}"; do
    if [ -d "$ROOT_DIR/$dir" ]; then
        echo "  📁 Copying $dir..."
        mkdir -p "$ASSETS_DIR/$dir"
        cp -RL "$ROOT_DIR/$dir/." "$ASSETS_DIR/$dir/" || {
            echo "  ⚠️ Warning: Some files in $dir could not be copied properly."
        }
    else
        echo "  ⚠️ Warning: $dir not found in root, skipping."
    fi
done

# Remove any .git files/folders if exist
echo "🧹 Cleaning up unwanted files..."
find "$ASSETS_DIR" -name ".git*" -type f -delete 2>/dev/null || true
find "$ASSETS_DIR" -name ".git" -type d -exec rm -rf {} + 2>/dev/null || true
find "$ASSETS_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

echo "✅ Assets synced successfully!"
echo "   Total: $(find "$ASSETS_DIR" -type f | wc -l | tr -d ' ') files"
