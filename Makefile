.PHONY: sync-dry sync sync-mcp apply-policy validate-agents install-hooks check sync-all bootstrap

sync-dry:
	agentsync apply --config agentsync.toml --dry-run --verbose

sync:
	agentsync apply --config agentsync.toml --verbose

sync-mcp:
	./scripts/sync-mcp.sh

apply-policy:
	./scripts/apply-policy.py

validate-agents:
	./scripts/validate-agents.rb

install-hooks:
	./scripts/install-hooks.sh

check:
	$(MAKE) validate-agents
	./scripts/check-links.sh

sync-all: sync sync-mcp apply-policy check

bootstrap: sync-all
