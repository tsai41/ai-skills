#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SOURCE_HOOK="$REPO_ROOT/.githooks/pre-commit"
TARGET_HOOK="$HOOKS_DIR/pre-commit"

if [[ ! -d "$HOOKS_DIR" ]]; then
  echo "[FAIL] git hooks directory not found: $HOOKS_DIR"
  exit 1
fi

chmod +x "$SOURCE_HOOK"
ln -sf "../../.githooks/pre-commit" "$TARGET_HOOK"
chmod +x "$TARGET_HOOK"

echo "[OK] installed pre-commit hook: $TARGET_HOOK -> $SOURCE_HOOK"
