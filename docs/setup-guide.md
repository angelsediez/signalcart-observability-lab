# Setup Guide

## Host Baseline

Target host:

- Ubuntu 24.04.4 LTS
- local homelab machine
- Docker Engine
- Docker Compose plugin
- k6

Phase 00 evidence is stored in:

```text
validation/host-baseline/
assets/screenshots/phase-00/
```

## Local Repository

Expected location:

```bash
~/projects/signalcart-observability-lab
```

Remote:

```text
git@github.com-signalcart:angelsediez/signalcart-observability-lab.git
```

## Required Host Tools

- git
- curl
- jq
- make
- tree
- python3
- pip3
- Docker Engine
- Docker Compose plugin
- k6

## Environment Variables

Use `.env.example` as the template for local configuration.

```bash
cp .env.example .env
```

Simulation endpoints are disabled by default:

```env
SIMULATION_MODE=false
```

To run incident simulations during the lab, set:

```env
SIMULATION_MODE=true
SIMULATION_TOKEN=your-local-token
```

## Running SignalCart API Locally

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install development dependencies:

```bash
python3 -m pip install -r requirements-dev.txt
```

Run the API locally:

```bash
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Validate health endpoints:

```bash
curl -s http://127.0.0.1:8000/health/live | jq .
curl -s http://127.0.0.1:8000/health/ready | jq .
```

Run the smoke test:

```bash
bash scripts/smoke-test.sh
```

Run tests:

```bash
python3 -m pytest -q
```

## PostgreSQL Local Database

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Check PostgreSQL readiness:

```bash
docker compose exec -T postgres pg_isready -U signalcart -d signalcart
```

Apply database migrations:

```bash
alembic upgrade head
```

Inspect tables:

```bash
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\\dt"
```

Run the API with PostgreSQL available:

```bash
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Validate readiness:

```bash
curl -s http://127.0.0.1:8000/health/ready | jq .
```

## Metrics Validation

Run the API locally:

```bash
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Check the metrics endpoint:

```bash
curl -s http://127.0.0.1:8000/metrics | grep '^signalcart_'
```

Validate database readiness metric:

```bash
curl -s http://127.0.0.1:8000/health/ready | jq .
curl -s http://127.0.0.1:8000/metrics | grep '^signalcart_database_ready'
```

Generate API traffic:

```bash
bash scripts/smoke-test.sh
```

Check domain counters:

```bash
curl -s http://127.0.0.1:8000/metrics \
  | grep -E 'signalcart_(products_created_total|orders_created_total|checkouts_completed_total|checkout_failures_total)'
```

## Running with Docker Compose and Nginx

Build the API image:

```bash
docker compose build api
```

Start the runtime:

```bash
docker compose up -d postgres api nginx
```

Apply database migrations from the API container:

```bash
docker compose exec -T api alembic upgrade head
```

Check container status:

```bash
docker compose ps
```

Validate the Nginx entrypoint:

```bash
curl -s http://127.0.0.1:8080/health/live | jq .
curl -s http://127.0.0.1:8080/health/ready | jq .
curl -s http://127.0.0.1:8080/version | jq .
```

Validate metrics through Nginx:

```bash
curl -s http://127.0.0.1:8080/metrics | grep '^signalcart_'
```

Run the Compose smoke test:

```bash
BASE_URL=http://127.0.0.1:8080 bash scripts/compose-smoke-test.sh
```

## Prometheus and Exporters

Start the metrics collection layer:

```bash
docker compose up -d \
  postgres \
  api \
  nginx \
  node-exporter \
  cadvisor \
  postgres-exporter \
  blackbox-exporter \
  prometheus
```

Validate Prometheus configuration:

```bash
docker compose run --rm --no-deps prometheus \
  promtool check config /etc/prometheus/prometheus.yml
```

Open Prometheus:

```text
http://127.0.0.1:9090
```

Open target status:

```text
http://127.0.0.1:9090/targets
```

Check targets from the command line:

```bash
bash scripts/check-prometheus-targets.sh
```

Query target health:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=up' \
  | jq .
```

Query SignalCart application metrics:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=signalcart_database_ready' \
  | jq .
```

Query PostgreSQL exporter:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=pg_up' \
  | jq .
```

Query Blackbox probe:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=probe_success{job="blackbox-nginx"}' \
  | jq .
```

Query representative exporter metrics:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=node_cpu_seconds_total' \
  | jq '.data.result[0:3]'

curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=container_cpu_usage_seconds_total' \
  | jq '.data.result[0:3]'
```

## Grafana Dashboards

Start Grafana with the runtime:

```bash
docker compose up -d \
  postgres \
  api \
  nginx \
  node-exporter \
  cadvisor \
  postgres-exporter \
  blackbox-exporter \
  prometheus \
  grafana
```

Open Grafana:

```text
http://127.0.0.1:3000
```

Default local credentials:

```text
admin / admin
```

Validate Grafana provisioning:

```bash
bash scripts/check-grafana-provisioning.sh
```

Validate Prometheus datasource:

```bash
curl -s -u admin:admin http://127.0.0.1:3000/api/datasources/name/Prometheus | jq .
```

List provisioned SignalCart dashboards:

```bash
curl -s -u admin:admin 'http://127.0.0.1:3000/api/search?query=SignalCart' | jq .
```

Recommended dashboard URLs:

```text
http://127.0.0.1:3000/d/signalcart-overview
http://127.0.0.1:3000/d/signalcart-api-red
http://127.0.0.1:3000/d/signalcart-infrastructure-use
http://127.0.0.1:3000/d/signalcart-postgres
http://127.0.0.1:3000/d/signalcart-synthetic-checks
```

## Alertmanager and Alert Rules

Start the alerting workflow:

```bash
docker compose up -d \
  postgres \
  api \
  nginx \
  node-exporter \
  cadvisor \
  postgres-exporter \
  blackbox-exporter \
  alertmanager \
  prometheus \
  grafana
```

Validate Prometheus alert rules:

```bash
docker compose run --rm --no-deps --entrypoint promtool prometheus \
  check rules \
  /etc/prometheus/rules/api-alerts.yml \
  /etc/prometheus/rules/postgres-alerts.yml \
  /etc/prometheus/rules/infrastructure-alerts.yml \
  /etc/prometheus/rules/synthetic-alerts.yml
```

Validate Alertmanager configuration:

```bash
docker compose run --rm --no-deps --entrypoint amtool alertmanager \
  check-config /etc/alertmanager/alertmanager.yml
```

Open Prometheus alerts:

```text
http://127.0.0.1:9090/alerts
```

Open Alertmanager:

```text
http://127.0.0.1:9093
```

Check alerts from the command line:

```bash
bash scripts/check-prometheus-alerts.sh
bash scripts/check-alertmanager.sh
```

## k6 Load Testing

Run the smoke load test:

```bash
BASE_URL=http://127.0.0.1:8080 k6 run \
  --summary-export validation/load-tests/P09-k6-smoke-summary.json \
  load-tests/smoke.js
```

Run the baseline load test:

```bash
BASE_URL=http://127.0.0.1:8080 k6 run \
  --summary-export validation/load-tests/P09-k6-baseline-summary.json \
  load-tests/baseline.js
```

Check Prometheus request rate after load:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=sum(rate(signalcart_http_requests_total[5m]))' \
  | jq .
```

Check p95 latency after load:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=histogram_quantile(0.95, sum by (le) (rate(signalcart_http_request_duration_seconds_bucket[5m])))' \
  | jq .
```

Check error percentage after load:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query \
  --data-urlencode 'query=100 * sum(rate(signalcart_http_requests_total{status_code=~"5.."}[5m])) / clamp_min(sum(rate(signalcart_http_requests_total[5m])), 0.001)' \
  | jq .
```

Check alert stability:

```bash
curl -s http://127.0.0.1:9090/api/v1/alerts | jq .
```

Open the API RED dashboard:

```text
http://127.0.0.1:3000/d/signalcart-api-red
```

## Evidence Locations

Text evidence:

```text
validation/
```

Screenshots:

```text
assets/screenshots/
```

Runbooks:

```text
runbooks/
```

Troubleshooting notes:

```text
troubleshooting/
```
