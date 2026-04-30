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

## Alert Review Questions

Before keeping an alert, answer:

- Does this alert represent user impact or a strong leading signal?
- Can an operator take action from the alert?
- Is the alert connected to a runbook?
- Is the expression understandable?
- Is the duration long enough to avoid noisy short spikes?
- Is the severity label meaningful?

## Example Alert Evidence Record

```text
Alert:
Symptom:
PromQL:
Expected state:
Observed state:
Dashboard:
Runbook:
Recovery action:
Validation after recovery:
Evidence files:
```
