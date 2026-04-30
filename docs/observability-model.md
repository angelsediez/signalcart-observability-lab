# Observability Model

## Goal

The lab should answer operational questions with evidence: is the service alive, is it ready, is the Nginx endpoint reachable, is Prometheus scraping targets, are exporters healthy, are dashboards showing live data, are errors increasing, is latency degrading, is PostgreSQL reachable, are containers under pressure, and is the synthetic probe succeeding.

## Health and Readiness

- `/health/live` confirms that the API process is alive.
- `/health/ready` confirms that the API is ready to serve traffic and validates PostgreSQL.

Expected healthy readiness response:

```json
{
  "status": "ready",
  "service": "SignalCart API",
  "dependencies": {
    "database": "ok"
  }
}
```

## Application Metrics

SignalCart API exposes Prometheus-compatible metrics at `GET /metrics`.

Application metrics include:

- `signalcart_http_requests_total`
- `signalcart_http_request_duration_seconds`
- `signalcart_http_requests_in_progress`
- `signalcart_products_created_total`
- `signalcart_orders_created_total`
- `signalcart_checkouts_completed_total`
- `signalcart_checkout_failures_total`
- `signalcart_database_ready`
- `signalcart_simulation_active`

## HTTP RED Metrics

RED means Rate, Errors, and Duration.

The API uses rate through `signalcart_http_requests_total`, errors through status-code labels, and duration through `signalcart_http_request_duration_seconds`.

Labels use method, route template, and status code. Raw URLs, query strings, product IDs, order IDs, request bodies, and user-provided values are avoided.

## Database and Simulation Metrics

`signalcart_database_ready` is `1` when database readiness is OK and `0` when readiness fails or the database readiness failure simulation is active.

Simulation state is exposed with `signalcart_simulation_active{simulation="..."}` for latency spike, error spike, and database readiness failure.

## Prometheus Metrics Collection

Collection jobs:

- `signalcart-api` collects application metrics.
- `node-exporter` collects host metrics.
- `cadvisor` collects container metrics.
- `postgres-exporter` collects PostgreSQL metrics.
- `blackbox-nginx` probes the Nginx readiness endpoint.
- `prometheus` collects Prometheus self-metrics.

Prometheus target health is validated through `http://127.0.0.1:9090/targets` and the `up` metric.

## Synthetic Probe Metrics

Blackbox Exporter provides `probe_success`, `probe_duration_seconds`, and `probe_http_status_code` for the Nginx entrypoint. Expected healthy result: `probe_success = 1`.

## Grafana Dashboards

Dashboard groups:

- SignalCart Overview
- API RED Metrics
- Infrastructure and Container Metrics
- PostgreSQL Metrics
- Synthetic Checks

Dashboards should answer operational questions: API scrape status, request rate, errors, p95 latency, PostgreSQL health, container resource usage, and synthetic Nginx readiness.

## Operational Workflow

Each incident simulation follows: hypothesis, experiment, metric observed, alert expected, evidence captured, diagnosis, recovery, and lesson learned.
