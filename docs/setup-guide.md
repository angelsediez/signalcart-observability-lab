# Setup Guide

## Host Baseline

Target host: Ubuntu 24.04.4 LTS on a local homelab machine with Docker Engine, Docker Compose plugin, Python, Git, jq, Make, and k6.

## Local Repository

Expected location:

```bash
~/projects/signalcart-observability-lab
```

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

## Running with Docker Compose and Nginx

```bash
docker compose build api
docker compose up -d postgres api nginx
docker compose exec -T api alembic upgrade head
```

Validate the Nginx entrypoint:

```bash
curl -s http://127.0.0.1:8080/health/live | jq .
curl -s http://127.0.0.1:8080/health/ready | jq .
curl -s http://127.0.0.1:8080/version | jq .
curl -s http://127.0.0.1:8080/metrics | grep '^signalcart_'
BASE_URL=http://127.0.0.1:8080 bash scripts/compose-smoke-test.sh
```

## Prometheus and Exporters

```bash
docker compose up -d   postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter prometheus
```

Validate Prometheus:

```bash
docker compose run --rm --no-deps prometheus   promtool check config /etc/prometheus/prometheus.yml
bash scripts/check-prometheus-targets.sh
```

Open:

```text
http://127.0.0.1:9090
http://127.0.0.1:9090/targets
```

Useful queries:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=up' | jq .
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=signalcart_database_ready' | jq .
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=pg_up' | jq .
curl -G -s http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=probe_success{job="blackbox-nginx"}' | jq .
```

## Grafana Dashboards

```bash
docker compose up -d   postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter prometheus grafana
```

Open Grafana:

```text
http://127.0.0.1:3000
```

Default local credentials:

```text
admin / admin
```

Validate:

```bash
bash scripts/check-grafana-provisioning.sh
curl -s -u admin:admin 'http://127.0.0.1:3000/api/search?query=SignalCart' | jq .
```

## Alertmanager and Alert Rules

```bash
docker compose up -d   postgres api nginx node-exporter cadvisor postgres-exporter blackbox-exporter alertmanager prometheus grafana
```

Validate Prometheus alert rules:

```bash
docker compose run --rm --no-deps --entrypoint promtool prometheus   check rules   /etc/prometheus/rules/api-alerts.yml   /etc/prometheus/rules/postgres-alerts.yml   /etc/prometheus/rules/infrastructure-alerts.yml   /etc/prometheus/rules/synthetic-alerts.yml
```

Validate Alertmanager configuration:

```bash
docker compose run --rm --no-deps --entrypoint amtool alertmanager   check-config /etc/alertmanager/alertmanager.yml
```

Open:

```text
http://127.0.0.1:9090/alerts
http://127.0.0.1:9093
```

Check alerts:

```bash
bash scripts/check-prometheus-alerts.sh
bash scripts/check-alertmanager.sh
```

## Evidence Locations

- Text evidence: `validation/`
- Screenshots: `assets/screenshots/`
- Runbooks: `runbooks/`
- Troubleshooting notes: `troubleshooting/`
