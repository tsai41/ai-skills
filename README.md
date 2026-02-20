# AI Hub

TL;DR:
- Run `make sync-all` from this directory to sync links, MCP, and policy.
- Shared source lives in `agents/` and `skills/`.
- AgentSync is required to apply these sync operations.

---

`ai-hub` is the user-level source of truth for shared AI setup.

It centralizes:
- shared `skills/`
- shared `agents/`
- MCP sync config
- permission policy defaults

## Prerequisite

This repository uses AgentSync to integrate and synchronize settings across AI tools.

- GitHub: https://github.com/dallay/agentsync
- Lib.rs: https://lib.rs/crates/agentsync

## Quick Start

Run from `ai-hub` root:

```bash
make sync-all
```

`make sync-all` runs the full pipeline:
- links sync (`agentsync.toml`)
- MCP sync (`../.agentsync-mcp.toml`)
- policy apply (`policy/user-policy.json`)
- link health check

Scope boundary:
- This repo manages user-level shared setup only.
- Project-specific instructions (for example per-repo `AGENTS.md`) should stay in each project.

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

## Layout

- `agents/`: shared agent definitions and prompts
- `skills/`: shared skills used by multiple tools
- `agentsync.toml`: link sync config for agents and skills
- `policy/user-policy.json`: permission policy definition
- `scripts/`: operational scripts (`sync-mcp.sh`, `apply-policy.py`, `check-links.sh`)

## Commands

Run from `ai-hub` root when you need partial operations:

```bash
make sync-dry
make sync
make sync-mcp
make apply-policy
make install-hooks
make check
make sync-all
```

Common path:
- Daily use: `make sync-all`
- Quick validation: `make check`
- Preview only: `make sync-dry`

Command intent:
- `make sync-dry`: preview link changes
- `make sync`: apply links from `agentsync.toml`
- `make sync-mcp`: sync MCP from `../.agentsync-mcp.toml` and merge OpenCode MCP into `.config/opencode/opencode.json`
- `make apply-policy`: apply permission policy from `policy/user-policy.json`
- `make install-hooks`: install repository git hooks (including pre-commit agent validation)
- `make check`: validate agent frontmatter schema and verify all managed links
- `make sync-all`: run full pipeline (`sync` + `sync-mcp` + `apply-policy` + `check`)
- `make bootstrap`: alias of `make sync-all`

## Permission Policy

`policy/user-policy.json` currently manages permission defaults only:
- Claude `settings.local.json`: read-only tool and read-only git/system command allowances
- Gemini `settings.json`: MCP server trust flags

Policy behavior:
- The policy script appends missing allowed items and does not remove existing entries.

## Troubleshooting

- `agentsync: command not found`: install AgentSync, then re-run `make sync-all`.
- OpenCode MCP not updated: run `make sync-mcp` and check `.config/opencode/opencode.json` has `mcp` entries.
- `make check` warns about `._old` folders: safe during migration; remove later if no rollback is needed.
