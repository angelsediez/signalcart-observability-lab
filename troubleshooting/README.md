# Troubleshooting Notes

This directory contains practical troubleshooting guides for common lab failures.

Troubleshooting notes are different from runbooks:

- runbooks are tied to alerts or incidents
- troubleshooting notes explain recurring operational problems and fixes

## Planned Troubleshooting Guides

```text
troubleshooting/
├── prometheus-targets-down.md
├── grafana-dashboard-missing-data.md
├── alertmanager-not-firing.md
└── exporter-common-errors.md
```

## Current Troubleshooting Checks

### Docker Compose services are not healthy

Check service status:

```bash
docker compose ps
```

Check logs:

```bash
docker compose logs --tail=120 api
docker compose logs --tail=120 nginx
docker compose logs --tail=120 postgres
```

### API container does not start

Check API logs:

```bash
docker compose logs --tail=120 api
```

Common causes:

- dependency missing from `requirements.txt`
- Python import error
- database connection error
- migration not applied

### Nginx returns 502

Check status:

```bash
docker compose ps
```

Check Nginx logs:

```bash
docker compose logs --tail=120 nginx
```

Check API logs:

```bash
docker compose logs --tail=120 api
```

Common causes:

- API container is not healthy
- API is not listening on `0.0.0.0`
- Nginx cannot reach the `api` service
- API startup failed

### Readiness returns 503

Check PostgreSQL:

```bash
docker compose exec -T postgres pg_isready -U signalcart -d signalcart
```

Check migrations:

```bash
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\dt"
```

Apply migrations:

```bash
docker compose exec -T api alembic upgrade head
```

### Metrics endpoint is empty or missing SignalCart metrics

Check endpoint:

```bash
curl -s http://127.0.0.1:8080/metrics | grep '^signalcart_'
```

Check API logs:

```bash
docker compose logs --tail=120 api
```

Run traffic:

```bash
BASE_URL=http://127.0.0.1:8080 bash scripts/compose-smoke-test.sh
```

Check domain counters:

```bash
curl -s http://127.0.0.1:8080/metrics \
  | grep -E 'signalcart_(products_created_total|orders_created_total|checkouts_completed_total)'
```

### Port 8080 is already in use

Check listener:

```bash
ss -ltnp | grep ':8080' || true
```

Stop the conflicting process or adjust the host port in `docker-compose.yml`.

### Reset local runtime

This removes local PostgreSQL data:

```bash
docker compose down -v
docker compose build api
docker compose up -d postgres api nginx
docker compose exec -T api alembic upgrade head
```

Use this when you need a clean lab state.

## Troubleshooting Note Template

```markdown
# Symptom

# Context

# Commands Used

# Evidence

# Root Cause

# Fix

# Prevention

# Documentation Updates
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
