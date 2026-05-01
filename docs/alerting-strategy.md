# Alerting Strategy

## Purpose

Alerts in this lab are designed to be actionable, understandable, and tied to runbooks.

An alert should answer what symptom is happening, why it matters, how long it has been happening, what to check first, and which runbook applies.

## Alertmanager Validation

Alertmanager is validated using Alertmanager UI, Prometheus alerts page, Prometheus API, Alertmanager API, validation files, and incident evidence.

## Implemented Alert Rules

Alert files:

- `alerts/api-alerts.yml`
- `alerts/postgres-alerts.yml`
- `alerts/infrastructure-alerts.yml`
- `alerts/synthetic-alerts.yml`

## API Alerts

- `APIScrapeDown`: Prometheus cannot scrape SignalCart API metrics.
- `APIHighErrorRate`: SignalCart API 5xx error percentage is elevated.
- `APIHighLatencyP95`: SignalCart API p95 latency is elevated.
- `DatabaseReadinessFailing`: SignalCart API reports database readiness failure.

## PostgreSQL Alerts

- `PostgresExporterDown`: Prometheus cannot scrape PostgreSQL Exporter.
- `PostgresDown`: PostgreSQL Exporter reports `pg_up = 0`.
- `PostgresTooManyConnections`: active database connections exceed the lab threshold.

## Infrastructure Alerts

- `HostHighCPU`: host CPU utilization is high for a sustained period.
- `HostLowMemory`: available host memory is low for a sustained period.
- `ContainerRestarting`: a container restart signal was detected.

## Synthetic Alerts

- `NginxEndpointDown`: Blackbox Exporter cannot probe the Nginx readiness endpoint successfully.
- `NginxHighProbeDuration`: Blackbox probe duration for Nginx readiness is elevated.

## Required Alert Metadata

Each alert includes:

- clear alert name
- PromQL expression
- `for:` duration
- severity label
- service label
- category label
- summary
- description
- runbook URL

## Alertmanager

Alertmanager runs locally at `http://127.0.0.1:9093`.

Alertmanager is validated through UI, API, Prometheus alert delivery, and controlled alert test evidence.

## Local Alert Validation

The controlled alert test uses the Nginx synthetic check:

1. Confirm `probe_success{job="blackbox-nginx"} = 1`
2. Stop Nginx
3. Wait for `NginxEndpointDown`
4. Confirm the alert appears in Prometheus
5. Confirm the alert appears in Alertmanager
6. Start Nginx
7. Confirm the probe recovers
8. Confirm the alert resolves

## Alert Evidence

Each alert validation should capture:

- Prometheus alert state
- Alertmanager alert view
- related Grafana panel when useful
- command output
- recovery validation

## Alert Review Questions

- Does this alert represent user impact or a strong leading signal?
- Can an operator take action from the alert?
- Is the alert connected to a runbook?
- Is the expression understandable?
- Is the duration long enough to avoid noisy short spikes?
- Is the severity label meaningful?
