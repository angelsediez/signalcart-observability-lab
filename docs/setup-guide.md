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

`~/projects/signalcart-observability-lab`

Remote:

`git@github.com-signalcart:angelsediez/signalcart-observability-lab.git`

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
