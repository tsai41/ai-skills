#!/usr/bin/env bash
set -euo pipefail

HUB_DIR="${HOME}/.ai-hub"

check_link() {
  local link_path="$1"
  local expected_target="$2"

  if [[ ! -L "$link_path" ]]; then
    echo "[FAIL] Missing symlink: $link_path"
    return 1
  fi

  local resolved
  resolved="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$link_path")"

  if [[ "$resolved" != "$expected_target" ]]; then
    echo "[FAIL] $link_path -> $resolved (expected: $expected_target)"
    return 1
  fi

  echo "[OK] $link_path -> $resolved"
}

echo "Checking shared links against ${HUB_DIR}"

check_link "${HOME}/.claude/agents" "${HUB_DIR}/agents"
check_link "${HOME}/.claude/skills" "${HUB_DIR}/skills"
check_link "${HOME}/.codex/skills" "${HUB_DIR}/skills"
check_link "${HOME}/.opencode/agent" "${HUB_DIR}/agents"
check_link "${HOME}/.opencode/skill" "${HUB_DIR}/skills"

for legacy in "${HOME}/.ai-agents._old" "${HOME}/.ai-skills._old"; do
  if [[ -e "$legacy" ]]; then
    echo "[WARN] Legacy backup still exists: $legacy"
  fi
done

echo "All required links are healthy."
