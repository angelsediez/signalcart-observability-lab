.PHONY: help test db-up db-down db-ps migrate smoke compose-build compose-up compose-down compose-ps compose-logs compose-smoke prom-up prom-targets prom-query-up grafana-up grafana-check alerts-up alerts-check load-smoke load-baseline load-stress load-evidence incidents incidents-summary final-check

help:
	@echo "SignalCart Observability Lab"
	@echo ""
	@echo "Available targets:"
	@echo "  make test             Run pytest"
	@echo "  make db-up            Start PostgreSQL"
	@echo "  make db-down          Stop PostgreSQL"
	@echo "  make db-ps            Show PostgreSQL container status"
	@echo "  make migrate          Apply Alembic migrations locally"
	@echo "  make smoke            Run API smoke test locally"
	@echo "  make compose-build    Build API image"
	@echo "  make compose-up       Start PostgreSQL, API, and Nginx"
	@echo "  make compose-down     Stop Compose runtime"
	@echo "  make compose-ps       Show Compose services"
	@echo "  make compose-logs     Show Compose logs"
	@echo "  make compose-smoke    Run smoke test through Nginx"
	@echo "  make prom-up          Start runtime with Prometheus and exporters"
	@echo "  make prom-targets     Show Prometheus target health"
	@echo "  make prom-query-up    Query Prometheus up metric"
	@echo "  make grafana-up       Start runtime with Grafana"
	@echo "  make grafana-check    Validate Grafana provisioning"
	@echo "  make alerts-up        Start runtime with Alertmanager"
	@echo "  make alerts-check     Validate Prometheus and Alertmanager alerts"
	@echo "  make load-smoke       Run k6 smoke load test"
	@echo "  make load-baseline    Run k6 baseline load test"
	@echo "  make load-stress      Run short controlled k6 stress test"
	@echo "  make load-evidence    Query load test evidence from Prometheus"
	@echo "  make incidents        Run incident simulation validation"
	@echo "  make incidents-summary Show incident validation summary"
	@echo "  make final-check      Run final local validation checks"

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

prom-up:
	docker compose up -d postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter prometheus

prom-targets:
	bash scripts/check-prometheus-targets.sh

prom-query-up:
	curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=up' | jq .

grafana-up:
	docker compose up -d postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter prometheus grafana

grafana-check:
	bash scripts/check-grafana-provisioning.sh

alerts-up:
	docker compose up -d postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter alertmanager prometheus grafana

alerts-check:
	bash scripts/check-prometheus-alerts.sh
	bash scripts/check-alertmanager.sh

load-smoke:
	BASE_URL=http://127.0.0.1:8080 k6 run --summary-export validation/load-tests/P09-k6-smoke-summary.json load-tests/smoke.js

load-baseline:
	BASE_URL=http://127.0.0.1:8080 k6 run --summary-export validation/load-tests/P09-k6-baseline-summary.json load-tests/baseline.js

load-stress:
	BASE_URL=http://127.0.0.1:8080 k6 run --summary-export validation/load-tests/P09-k6-stress-summary.json load-tests/stress.js

load-evidence:
	bash scripts/check-load-test-evidence.sh

incidents:
	BASE_URL=http://127.0.0.1:8080 PROMETHEUS_URL=http://127.0.0.1:9090 SIMULATION_TOKEN=local-simulation-token bash scripts/run-incident-simulation.sh

incidents-summary:
	cat validation/incidents/P10-incident-validation-summary.txt

final-check:
	python3 -m pytest -q
	docker compose config -q
	git diff --check
