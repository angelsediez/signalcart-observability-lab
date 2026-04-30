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
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\dt"
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
