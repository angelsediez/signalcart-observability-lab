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

## Health and Readiness Endpoints

SignalCart API exposes two health endpoints:

- `/health/live` confirms that the API process is alive.
- `/health/ready` confirms that the API is ready to serve traffic.

The readiness endpoint validates PostgreSQL with a lightweight database query.

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

## Application Metric Names

Planned and implemented application metrics include:

- `signalcart_http_requests_total`
- `signalcart_http_request_duration_seconds`
- `signalcart_http_requests_in_progress`
- `signalcart_products_created_total`
- `signalcart_orders_created_total`
- `signalcart_checkouts_completed_total`
- `signalcart_checkout_failures_total`
- `signalcart_database_ready`
- `signalcart_simulation_active`

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

## Synthetic Monitoring

The Nginx entrypoint provides a stable path for synthetic checks:

```text
http://127.0.0.1:8080/health/ready
```

Synthetic checks validate the service from the outside, instead of only trusting internal application metrics.

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

For this lab, USE is applied to host and container metrics when infrastructure metrics collection is added.

## PostgreSQL Monitoring

PostgreSQL is validated by:

- API readiness checks
- SQL query validation
- migration evidence
- application metrics
- runtime container health

Database signals include:

- database availability
- schema migration state
- stored products and orders
- readiness behavior from the API

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

## Prometheus Metrics Collection

Prometheus collects metrics from the application and exporters.

Collection jobs:

- `signalcart-api` collects application metrics from `/metrics`
- `node-exporter` collects host metrics
- `cadvisor` collects container metrics
- `postgres-exporter` collects PostgreSQL metrics
- `blackbox-nginx` probes the Nginx readiness endpoint
- `prometheus` collects Prometheus self-metrics

## Target Health

Prometheus target health is validated through:

```text
http://127.0.0.1:9090/targets
```

The `up` metric is used to verify whether Prometheus can scrape each target.

Examples:

```promql
up
up{job="signalcart-api"}
up{job="node-exporter"}
up{job="cadvisor"}
up{job="postgres-exporter"}
```

## Synthetic Probe Metrics

Blackbox Exporter provides synthetic check metrics for the Nginx entrypoint.

Important metrics:

```promql
probe_success{job="blackbox-nginx"}
probe_duration_seconds{job="blackbox-nginx"}
probe_http_status_code{job="blackbox-nginx"}
```

Expected healthy result:

```text
probe_success = 1
```

## Exporter Metrics

Representative exporter metrics:

```promql
node_cpu_seconds_total
container_cpu_usage_seconds_total
pg_up
```

These metrics help connect API behavior with host, container, and database signals.
