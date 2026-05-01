.PHONY: load-smoke load-baseline load-stress load-evidence  help test db-up db-down db-ps migrate smoke compose-build compose-up compose-down compose-ps compose-logs compose-smoke

help:
	@echo "SignalCart Observability Lab"
	@echo ""
	@echo "Available targets:"
	@echo "  make test           Run pytest"
	@echo "  make db-up          Start PostgreSQL"
	@echo "  make db-down        Stop PostgreSQL"
	@echo "  make db-ps          Show PostgreSQL container status"
	@echo "  make migrate        Apply Alembic migrations locally"
	@echo "  make smoke          Run API smoke test locally"
	@echo "  make compose-build  Build API image"
	@echo "  make compose-up     Start PostgreSQL, API, and Nginx"
	@echo "  make compose-down   Stop Compose runtime"
	@echo "  make compose-ps     Show Compose services"
	@echo "  make compose-logs   Show Compose logs"
	@echo "  make compose-smoke  Run smoke test through Nginx"

test:
	python3 -m pytest -q

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

compose-build:
	docker compose build api

compose-up:
	docker compose up -d postgres api nginx

compose-down:
	docker compose down

compose-ps:
	docker compose ps

compose-logs:
	docker compose logs --tail=100

compose-smoke:
	BASE_URL=http://127.0.0.1:8080 bash scripts/compose-smoke-test.sh


grafana-up:
	docker compose up -d postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter prometheus grafana

grafana-check:
	bash scripts/check-grafana-provisioning.sh


load-smoke:
	BASE_URL=http://127.0.0.1:8080 k6 run --summary-export validation/load-tests/P09-k6-smoke-summary.json load-tests/smoke.js

load-baseline:
	BASE_URL=http://127.0.0.1:8080 k6 run --summary-export validation/load-tests/P09-k6-baseline-summary.json load-tests/baseline.js

load-stress:
	BASE_URL=http://127.0.0.1:8080 k6 run --summary-export validation/load-tests/P09-k6-stress-summary.json load-tests/stress.js

load-evidence:
	bash scripts/check-load-test-evidence.sh
