#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_CONFIG="${ROOT_DIR}/../.agentsync-mcp.toml"

agentsync apply --config "${MCP_CONFIG}" --verbose

SOURCE_OPENCODE_JSON="${HOME}/opencode.json"
TARGET_OPENCODE_JSON="${HOME}/.config/opencode/opencode.json"

if [[ -f "${SOURCE_OPENCODE_JSON}" && -f "${TARGET_OPENCODE_JSON}" ]]; then
  python3 - <<'PY'
import json
import os
from pathlib import Path

source_path = Path(os.path.expanduser("~/opencode.json"))
target_path = Path(os.path.expanduser("~/.config/opencode/opencode.json"))

with source_path.open("r", encoding="utf-8") as f:
    source = json.load(f)

with target_path.open("r", encoding="utf-8") as f:
    target = json.load(f)

target["mcp"] = source.get("mcp", {})

with target_path.open("w", encoding="utf-8") as f:
    json.dump(target, f, indent=2)
    f.write("\n")
PY

  rm -f "${SOURCE_OPENCODE_JSON}"
  echo "Synced MCP into ${TARGET_OPENCODE_JSON} and removed ${SOURCE_OPENCODE_JSON}."
fi
