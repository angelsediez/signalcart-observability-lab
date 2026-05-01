# Observability Model

## Goal

The lab should answer operational questions with evidence:

- Is the service alive?
- Is the service ready?
- Is the Nginx-exposed endpoint reachable?
- Is Prometheus scraping the app?
- Are exporters healthy?
- Are dashboards showing live data?
- Are alert rules loaded?
- Is Alertmanager receiving alerts?
- Is request rate normal?
- Are errors increasing?
- Is latency degrading?
- Is PostgreSQL reachable?
- Are host or container resources under pressure?
- Is the synthetic probe succeeding?
- Did recovery resolve the symptom?

## Health and Readiness Endpoints

`/health/live` confirms process health. `/health/ready` validates PostgreSQL readiness.

Healthy readiness response:

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

The API uses RED-style HTTP metrics:

- Rate through `signalcart_http_requests_total`
- Errors through status-code labels
- Duration through `signalcart_http_request_duration_seconds`

Labels stay low-cardinality: `method`, `route`, and `status_code`.

## Database Readiness Metric

`signalcart_database_ready` uses `1` for ready and `0` for failed readiness or simulated readiness failure.

## Simulation Metrics

Simulation state is exposed through `signalcart_simulation_active` with known simulation labels: `latency_spike`, `error_spike`, and `db_readiness_failure`.

## Prometheus Metrics Collection

Collection jobs:

- `signalcart-api` collects application metrics from `/metrics`
- `node-exporter` collects host metrics
- `cadvisor` collects container metrics
- `postgres-exporter` collects PostgreSQL metrics
- `blackbox-nginx` probes the Nginx readiness endpoint
- `prometheus` collects Prometheus self-metrics

Prometheus target health is validated through `http://127.0.0.1:9090/targets` and the `up` metric.

## Synthetic Probe Metrics

Blackbox Exporter provides:

- `probe_success{job="blackbox-nginx"}`
- `probe_duration_seconds{job="blackbox-nginx"}`
- `probe_http_status_code{job="blackbox-nginx"}`

Healthy result: `probe_success = 1`.

## Grafana Dashboards

Dashboard groups:

- SignalCart Overview
- API RED Metrics
- Infrastructure and Container Metrics
- PostgreSQL Metrics
- Synthetic Checks

Dashboards should answer operational questions and avoid unnecessary clutter.

## Alerting Workflow

Prometheus evaluates alert rules from files under `alerts/`. When an alert fires, Prometheus sends it to Alertmanager.

Alertmanager provides alert grouping, deduplication, state visibility, UI validation, and API validation.

Every alert includes severity, summary, description, and runbook URL.

## Dashboard and Alert Design Rules

Useful dashboards and alerts answer specific operational questions:

- Is the API being scraped?
- Is request rate changing?
- Are errors increasing?
- Is p95 latency degrading?
- Is PostgreSQL up?
- Are containers consuming CPU or memory?
- Is the synthetic Nginx readiness probe succeeding?
- Is there a runbook for the alert?

## Label Cardinality

Good labels are stable and bounded: HTTP method, route template, status code, simulation name, job, and instance.

Avoid raw URLs, query strings, product IDs, order IDs, user-provided text, and request body values.

## Operational Workflow

Each incident simulation follows this cycle:

1. Hypothesis
2. Experiment
3. Metric observed
4. Alert expected
5. Evidence captured
6. Diagnosis
7. Recovery
8. Lesson learned
