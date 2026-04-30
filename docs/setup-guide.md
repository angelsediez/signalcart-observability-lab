# Setup Guide

## Host Baseline

Target host: Ubuntu 24.04.4 LTS local homelab machine with Docker Engine, Docker Compose plugin, and k6.

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

Use `.env.example` as the template for local configuration. Simulation endpoints are disabled by default with `SIMULATION_MODE=false`.

## Running SignalCart API Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Validate:

```bash
curl -s http://127.0.0.1:8000/health/live | jq .
curl -s http://127.0.0.1:8000/health/ready | jq .
bash scripts/smoke-test.sh
python3 -m pytest -q
```

## PostgreSQL Local Database

```bash
docker compose up -d postgres
docker compose exec -T postgres pg_isready -U signalcart -d signalcart
alembic upgrade head
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\dt"
```

## Metrics Validation

```bash
curl -s http://127.0.0.1:8000/metrics | grep '^signalcart_'
curl -s http://127.0.0.1:8000/metrics | grep '^signalcart_database_ready'
bash scripts/smoke-test.sh
```

## Running with Docker Compose and Nginx

```bash
docker compose build api
docker compose up -d postgres api nginx
docker compose exec -T api alembic upgrade head
docker compose ps
```

Validate Nginx entrypoint:

```bash
curl -s http://127.0.0.1:8080/health/live | jq .
curl -s http://127.0.0.1:8080/health/ready | jq .
curl -s http://127.0.0.1:8080/version | jq .
curl -s http://127.0.0.1:8080/metrics | grep '^signalcart_'
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
docker compose run --rm --no-deps prometheus promtool check config /etc/prometheus/prometheus.yml
```

Open Prometheus: `http://127.0.0.1:9090`

Open target status: `http://127.0.0.1:9090/targets`

Check targets from the command line:

```bash
bash scripts/check-prometheus-targets.sh
```

Query key metrics:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=up' | jq .
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=signalcart_database_ready' | jq .
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=pg_up' | jq .
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=probe_success{job="blackbox-nginx"}' | jq .
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

Open Grafana: `http://127.0.0.1:3000`

Default local credentials: `admin / admin`

Validate Grafana provisioning:

```bash
bash scripts/check-grafana-provisioning.sh
curl -s -u admin:admin http://127.0.0.1:3000/api/datasources/name/Prometheus | jq .
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

## Evidence Locations

Text evidence: `validation/`

Screenshots: `assets/screenshots/`

Runbooks: `runbooks/`

Troubleshooting notes: `troubleshooting/`
