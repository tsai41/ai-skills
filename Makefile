.PHONY: sync-dry sync check bootstrap

sync-dry:
	agentsync apply --config agentsync.toml --dry-run --verbose

sync:
	agentsync apply --config agentsync.toml --verbose

sync-mcp:
	./scripts/sync-mcp.sh

apply-policy:
	./scripts/apply-policy.py

check:
	./scripts/check-links.sh

sync-all: sync sync-mcp apply-policy check

bootstrap: sync-all
