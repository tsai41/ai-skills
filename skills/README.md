# AI Skills

This folder contains the shared skills used by multiple AI tools.

## Usage

All supported tools should reference this same directory via symlink managed by
AgentSync.

Example target paths:

- `.claude/skills`
- `.codex/skills`
- `.opencode/skill`

## Reference

Claude skills documentation:
https://code.claude.com/docs/en/skills

Discovery catalogs:
https://claude-plugins.dev/skills
https://www.aitmpl.com/skills

## Setup

If this folder is version-controlled, enable repository hooks when needed:

```bash
git config core.hooksPath .githooks
```
