# AI Hub

`ai-hub` is the user-level source of truth for shared AI setup.

It centralizes:
- shared `skills/`
- shared `agents/`
- MCP sync config
- permission policy defaults

## Layout

- `agents/`: shared agent definitions and prompts
- `skills/`: shared skills used by multiple tools
- `agentsync.toml`: link sync config for agents and skills
- `policy/user-policy.json`: permission policy definition
- `scripts/`: operational scripts (`sync-mcp.sh`, `apply-policy.py`, `check-links.sh`)

## Synced Targets

### Skills

- `.claude/skills`
- `.codex/skills`
- `.cursor/skills-cursor`
- `.gemini/antigravity/skills`
- `.opencode/skill`

### Agents

- `.claude/agents`
- `.opencode/agent`

## AgentSync Links

- GitHub: https://github.com/dallay/agentsync
- Lib.rs: https://lib.rs/crates/agentsync

## Daily Workflow

Run from `ai-hub` root:

```bash
make sync-dry
make sync
make sync-mcp
make apply-policy
make check
make sync-all
```

Command intent:
- `make sync-dry`: preview link changes
- `make sync`: apply links from `agentsync.toml`
- `make sync-mcp`: sync MCP from `../.agentsync-mcp.toml` and merge OpenCode MCP into `.config/opencode/opencode.json`
- `make apply-policy`: apply permission policy from `policy/user-policy.json`
- `make check`: verify all managed links
- `make sync-all`: run full pipeline (`sync` + `sync-mcp` + `apply-policy` + `check`)
- `make bootstrap`: alias of `make sync-all`

## Policy Scope

`policy/user-policy.json` currently manages permission defaults only:
- Claude `settings.local.json`: read-only tool and read-only git/system command allowances
- Gemini `settings.json`: MCP server trust flags
