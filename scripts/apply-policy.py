#!/usr/bin/env python3
import json
from pathlib import Path


def read_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def ensure_claude_permissions(home: Path, policy: dict):
    settings_path = home / ".claude" / "settings.local.json"
    settings = read_json(settings_path, {})

    permissions = settings.setdefault("permissions", {})
    allow = permissions.setdefault("allow", [])
    allow_set = set(allow)

    for item in policy.get("permissionsAllow", []):
        if item not in allow_set:
            allow.append(item)
            allow_set.add(item)

    write_json(settings_path, settings)
    return settings_path


def ensure_gemini_mcp_trust(home: Path, policy: dict):
    settings_path = home / ".gemini" / "settings.json"
    settings = read_json(settings_path, {})

    if policy.get("forceMcpTrust"):
        servers = settings.get("mcpServers", {})
        for _, server_cfg in servers.items():
            if isinstance(server_cfg, dict):
                server_cfg["trust"] = True

    write_json(settings_path, settings)
    return settings_path


def main():
    hub_dir = Path(__file__).resolve().parent.parent
    policy_path = hub_dir / "policy" / "user-policy.json"
    policy = read_json(policy_path, {})
    home = Path.home()

    updated = []
    claude_policy = policy.get("claude", {})
    gemini_policy = policy.get("gemini", {})

    updated.append(str(ensure_claude_permissions(home, claude_policy)))

    updated.append(str(ensure_gemini_mcp_trust(home, gemini_policy)))

    print("Applied user policy to:")
    for path in updated:
        print(f"- {path}")


if __name__ == "__main__":
    main()
