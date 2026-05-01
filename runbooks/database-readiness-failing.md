# DatabaseReadinessFailing Runbook

## Symptom

SignalCart API reports database readiness failure.

## Impact

The API process may be alive but not ready for database-backed traffic.

## First Checks

```bash
docker compose ps
docker compose logs --tail=120 api
docker compose logs --tail=120 nginx
docker compose logs --tail=120 postgres
curl -s http://127.0.0.1:8080/health/live | jq .
curl -s http://127.0.0.1:8080/health/ready | jq .
```

## Diagnosis Steps

Check the main metric:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query   --data-urlencode 'query=signalcart_database_ready' | jq .
```

Check Prometheus alerts:

```bash
bash scripts/check-prometheus-alerts.sh
```

Check Alertmanager alerts:

```bash
bash scripts/check-alertmanager.sh
```

Check relevant dashboards in Grafana:

```text
http://127.0.0.1:3000
```

## Recovery Steps

Recommended recovery action:

```text
recover DB simulation or start PostgreSQL
```

Use the least destructive action first. Capture evidence before restarting services.

## Recovery Validation

Run the main metric query again:

```bash
curl -G -s http://127.0.0.1:9090/api/v1/query   --data-urlencode 'query=signalcart_database_ready' | jq .
```

Validate the public readiness endpoint:

```bash
curl -s http://127.0.0.1:8080/health/ready | jq .
```

Confirm the alert is no longer firing:

```bash
bash scripts/check-prometheus-alerts.sh
bash scripts/check-alertmanager.sh
```

## Evidence to Capture

- command output before recovery
- Prometheus alert state
- Alertmanager alert state
- Grafana screenshot when useful
- recovery command output
- command output after recovery
- short lesson learned
