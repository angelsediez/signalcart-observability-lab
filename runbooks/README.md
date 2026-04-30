# Runbooks

Runbooks describe how to investigate and recover from specific alerts or incidents.

Each runbook should be practical, short enough to follow during pressure, and specific enough to produce evidence.

## Runbook Structure

Each runbook should include:

1. Alert or symptom
2. User impact
3. First checks
4. Diagnosis steps
5. Recovery steps
6. Validation steps
7. Evidence to capture
8. Notes and follow-up actions

## Planned Runbooks

```text
runbooks/
├── api-high-latency.md
├── api-high-error-rate.md
├── postgres-down.md
├── nginx-down.md
└── alertmanager-triage.md
```

## Current Operational Checks

Before alerting infrastructure is added, use these checks manually.

### API liveness

```bash
curl -s http://127.0.0.1:8080/health/live | jq .
```

Expected:

```json
{
  "status": "ok",
  "service": "SignalCart API"
}
```

### API readiness

```bash
curl -s http://127.0.0.1:8080/health/ready | jq .
```

Expected:

```json
{
  "status": "ready",
  "service": "SignalCart API",
  "dependencies": {
    "database": "ok"
  }
}
```

### Metrics endpoint

```bash
curl -s http://127.0.0.1:8080/metrics | grep '^signalcart_'
```

### Compose status

```bash
docker compose ps
```

Expected services:

- `signalcart-postgres`
- `signalcart-api`
- `signalcart-nginx`

### API logs

```bash
docker compose logs --tail=100 api
```

### Nginx logs

```bash
docker compose logs --tail=100 nginx
```

### PostgreSQL readiness

```bash
docker compose exec -T postgres pg_isready -U signalcart -d signalcart
```

## Evidence Checklist

For each incident or validation run, capture:

- command used
- command output
- screenshot when useful
- affected endpoint
- observed metric
- recovery command
- validation after recovery
- lesson learned

Store text evidence under:

```text
validation/incidents/
```

Store screenshots under:

```text
assets/screenshots/
```

## Runbook Quality Checklist

A useful runbook should:

- start with symptoms, not assumptions
- include safe first checks
- avoid destructive commands unless clearly marked
- explain how to validate recovery
- reference evidence files
- be updated after each incident simulation
