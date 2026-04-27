# Alerting Strategy

## Purpose

Alerts in this lab are designed to be actionable, understandable, and tied to runbooks.

An alert should answer:

- What symptom is happening?
- Why does it matter?
- How long has it been happening?
- What should the operator check first?
- Which runbook applies?

## Alertmanager Validation

Alertmanager is validated using:

- Alertmanager UI
- Prometheus alerts page
- Grafana screenshots
- validation files
- incident evidence

## Planned Alert Groups

### API

- `APIDown`
- `ReadinessCheckFailing`
- `APIHighErrorRate`
- `APIHighLatencyP95`

### Database

- `PostgresDown`
- `PostgresTooManyConnections`
- `DatabaseReadinessFailing`

### Infrastructure

- `HostHighCPU`
- `HostLowMemory`
- `HostLowDiskSpace`
- `ContainerRestarting`

### Synthetic Checks

- `BlackboxProbeFailing`
- `NginxEndpointDown`

## Required Alert Metadata

Each alert should include:

- clear alert name
- PromQL expression
- `for:` duration
- severity label
- summary
- description
- runbook URL when available

## Alert Evidence

Each alert validation should capture:

- Prometheus alert state
- Alertmanager alert view
- related Grafana panel
- command output when useful
- recovery validation
