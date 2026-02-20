.PHONY: sync-dry sync check bootstrap

sync-dry:
	agentsync apply --config agentsync.toml --dry-run --verbose

sync:
	agentsync apply --config agentsync.toml --verbose

sync-mcp:
	./scripts/sync-mcp.sh

check:
	./scripts/check-links.sh

bootstrap: sync-dry check
