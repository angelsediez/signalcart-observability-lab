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