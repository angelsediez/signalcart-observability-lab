# Validation Evidence

This directory stores evidence generated while building and operating the lab.

Evidence should be small, text-based when possible, and tied to a documented phase or incident.

## Evidence Types

Examples:

- host baseline outputs
- API baseline outputs
- database migration outputs
- PostgreSQL schema outputs
- metrics endpoint captures
- Docker Compose runtime outputs
- smoke test outputs
- alert validation results
- incident simulation outputs
- load test results

## Directory Layout

```text
validation/
├── host-baseline/
├── api-baseline/
├── database-baseline/
├── metrics-baseline/
├── compose-runtime/
├── prometheus-targets/
├── alert-tests/
├── incidents/
└── load-tests/
```

## Naming Convention

Evidence files use this pattern:

```text
PXX-description.txt
PXX-description.json
```

Examples:

```text
P02-pytest-output.txt
P03-alembic-upgrade-head.txt
P04-metrics-after-smoke-test.txt
P05-compose-smoke-test-output.txt
```

## Evidence Quality Checklist

Good evidence should show:

- command output
- service status
- expected result
- timestamp when useful
- validation result
- enough context to reproduce the check

Avoid storing:

- secrets
- tokens
- private keys
- large binary artifacts
- local-only temporary files

## Relationship with Screenshots

Text evidence lives here.

Visual evidence lives under:

```text
assets/screenshots/
```

Both are useful. Text evidence is better for review and diffing. Screenshots are useful for GitHub presentation and interview discussion.
