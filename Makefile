.PHONY: help test db-up db-down db-ps migrate smoke

help:
	@echo "SignalCart Observability Lab"
	@echo ""
	@echo "Available targets:"
	@echo "  make test      Run pytest"
	@echo "  make db-up     Start PostgreSQL"
	@echo "  make db-down   Stop PostgreSQL"
	@echo "  make db-ps     Show PostgreSQL container status"
	@echo "  make migrate   Apply Alembic migrations"
	@echo "  make smoke     Run API smoke test"

test:
	pytest -q

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

db-ps:
	docker compose ps

migrate:
	alembic upgrade head

smoke:
	bash scripts/smoke-test.sh
