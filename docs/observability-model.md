# Observability Model

## Goal

The lab should answer operational questions with evidence:

- Is the service alive?
- Is the service ready?
- Is the Nginx-exposed endpoint reachable?
- Is request rate normal?
- Are errors increasing?
- Is latency degrading?
- Is PostgreSQL reachable?
- Are host or container resources under pressure?
- Did the expected alert appear?
- Did recovery resolve the symptom?

## Application Metrics

Planned application metrics:

- `http_requests_total`
- `http_request_duration_seconds`
- `http_requests_in_progress`
- `http_errors_total`
- `app_build_info`
- `app_database_ready`
- `checkout_requests_total`
- `checkout_failures_total`

## API RED Dashboard Model

RED means:

- Rate
- Errors
- Duration

For SignalCart API, RED is applied to HTTP endpoints and checkout behavior.

## Infrastructure USE Dashboard Model

USE means:

- Utilization
- Saturation
- Errors

For this lab, USE is applied to host and container metrics.

## PostgreSQL Monitoring

PostgreSQL metrics are collected with PostgreSQL Exporter.

Planned database signals:

- database availability
- active connections
- transactions
- rollbacks
- database size
- readiness behavior from the API

## Synthetic Monitoring

Blackbox Exporter validates the endpoint exposed through Nginx.

Planned synthetic metrics:

- `probe_success`
- `probe_duration_seconds`
- `probe_http_status_code`

Synthetic monitoring complements internal application metrics by checking the service from the outside.

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
## Health and Readiness Endpoints

SignalCart API exposes two health endpoints:

- `/health/live` confirms that the API process is alive.
- `/health/ready` confirms that the API is ready to serve traffic.

The readiness response currently reports the database dependency as `not_configured`. Database-backed readiness is added when PostgreSQL is connected.

## Database-Backed Readiness

The readiness endpoint validates PostgreSQL with a lightweight database query.

Expected healthy response:

```json
{
  "status": "ready",
  "service": "SignalCart API",
  "dependencies": {
    "database": "ok"
  }
}
```

The liveness endpoint remains independent from PostgreSQL. This distinction helps separate process health from dependency readiness.

## Application Metrics

SignalCart API exposes Prometheus-compatible application metrics at:

```text
GET /metrics
```

These metrics describe API traffic, latency, errors, domain activity, database readiness, and lab simulation state.

## HTTP RED Metrics

The API exposes RED-style HTTP metrics:

- Rate through `signalcart_http_requests_total`
- Errors through status-code labels on `signalcart_http_requests_total`
- Duration through `signalcart_http_request_duration_seconds`

The request metrics use low-cardinality labels:

- `method`
- `route`
- `status_code`

The `route` label uses route templates instead of raw URLs.

## Domain Metrics

SignalCart exposes domain counters for key API actions:

- `signalcart_products_created_total`
- `signalcart_orders_created_total`
- `signalcart_checkouts_completed_total`
- `signalcart_checkout_failures_total`

These counters make checkout behavior visible during load tests and incident simulations.

## Database Readiness Metric

Database readiness is exposed as:

```text
signalcart_database_ready
```

Expected values:

- `1` means database readiness is OK.
- `0` means database readiness failed or the database readiness failure simulation is active.

## Simulation Metrics

Simulation state is exposed as:

```text
signalcart_simulation_active{simulation="latency_spike"}
signalcart_simulation_active{simulation="error_spike"}
signalcart_simulation_active{simulation="db_readiness_failure"}
```

A value of `1` means the simulation is active. A value of `0` means it is inactive.

## Label Cardinality

Metric labels must avoid high cardinality.

Good labels:

- HTTP method
- route template
- status code
- known simulation name

Avoid labels such as:

- raw full URL
- query string
- product ID
- order ID
- user-provided text
- request body values

Low-cardinality labels keep metrics useful, queryable, and safe to aggregate.
