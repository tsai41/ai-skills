# AI Hub

This directory is the single source of truth for shared AI configuration at the
user level.

## Structure

- `agents/`: Shared agent definitions and prompts
- `skills/`: Shared skills consumed by multiple AI tools
- `agentsync.toml`: Synchronization rules for tool-specific target paths

## User-Level Sync Targets

Current shared skills targets:

- `.claude/skills`
- `.codex/skills`
- `.opencode/skill`

Each target is managed by AgentSync and points to the same shared skills source.

## Install AgentSync

Project links:

- GitHub: https://github.com/dallay/agentsync
- Lib.rs: https://lib.rs/crates/agentsync

Install options:

```bash
# npm (global)
npm install -g @dallay/agentsync

# or Rust
cargo install agentsync
```

## AgentSync Usage

From the `ai-hub` root directory:

```bash
agentsync apply --config agentsync.toml --dry-run --verbose
agentsync apply --config agentsync.toml --verbose
```

## Migration Note

Legacy locations:

- `.ai-agents`
- `.ai-skills`

During transition, keep legacy paths compatible (symlink or redirect docs) until
all scripts and GitHub repo paths are updated.
