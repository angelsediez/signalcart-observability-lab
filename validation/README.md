# Validation Evidence

This directory stores operational evidence generated while building and validating SignalCart Observability Lab.

Evidence should be small, reviewable, and tied to a phase or incident.

## Evidence Areas

```text
validation/
├── host-baseline/
├── api-baseline/
├── database-baseline/
├── metrics-baseline/
├── compose-runtime/
├── prometheus-targets/
├── grafana-dashboards/
├── alert-tests/
├── load-tests/
└── incidents/
```

## Evidence Types

Examples:

- command outputs
- JSON responses
- Prometheus query results
- k6 summaries
- alert state captures
- incident before/during/after records
- recovery validation outputs

## Incident Evidence

Incident evidence lives under:

```text
validation/incidents/
```

Incident evidence should show:

1. healthy state before the incident
2. observed signal during the incident
3. recovery action
4. healthy state after recovery

## Evidence Rules

Do not store secrets, tokens, private keys, large binaries, or unrelated local files.

Screenshots live under:

```text
assets/screenshots/
```
