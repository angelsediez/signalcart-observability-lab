# SignalCart Observability Lab

SignalCart Observability Lab is a local-first observability homelab for practicing practical SRE operations with a small FastAPI checkout/cart service.

The lab demonstrates how to instrument, monitor, validate metrics collection, troubleshoot, and recover a service using a metrics-driven observability workflow.

## What This Lab Demonstrates

- API health and readiness checks
- Application metrics
- Prometheus-compatible metrics exposition
- Prometheus metrics collection
- Prometheus target validation
- Host metrics with Node Exporter
- Container metrics with cAdvisor
- PostgreSQL metrics with PostgreSQL Exporter
- Synthetic endpoint checks with Blackbox Exporter
- Docker Compose runtime validation
- Nginx reverse proxy validation
- PostgreSQL-backed persistence
- SQLAlchemy data access
- Alembic database migrations
- pytest-based validation
- Synthetic-ready HTTP entrypoint
- Load testing preparation with k6
- Controlled incident simulations
- Runbook-driven troubleshooting
- Recovery validation
- Evidence-based operational documentation

## Service Under Observation

The application under observation is **SignalCart API**, a small checkout/cart API with products, orders, checkout, health checks, metrics, and controlled incident simulation endpoints.

The application is intentionally simple so the main focus stays on observability, SRE operations, incident response, and troubleshooting.

Application endpoints:

- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- `GET /metrics`
- `GET /products`
- `POST /products`
- `GET /orders`
- `POST /orders`
- `POST /checkout`

Lab simulation endpoints:

- `POST /lab/simulations/latency-spike`
- `POST /lab/simulations/error-spike`
- `POST /lab/simulations/db-readiness-failure`
- `POST /lab/simulations/recover`

Simulation endpoints are disabled by default and only work when:

```env
SIMULATION_MODE=true
```

They also require:

```env
SIMULATION_TOKEN
```

## Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- pytest
- Nginx
- Docker Compose
- Prometheus-compatible application metrics
- Prometheus
- prometheus-client
- Node Exporter
- cAdvisor
- PostgreSQL Exporter
- Blackbox Exporter
- k6
- Bash scripts
- runbooks
- troubleshooting docs
- validation evidence
- screenshots

## Architecture

```text
User / curl / k6
        |
        v
      Nginx
        |
        v
 SignalCart API - FastAPI
        |
        v
   PostgreSQL
```

## Observability Workflow

```text
SignalCart API /metrics
        |
        v
Prometheus-compatible metrics endpoint

Nginx-exposed API endpoint
        |
        v
Synthetic monitoring ready path
```

The API exposes application metrics in Prometheus text format at `/metrics`. The endpoint is reachable through Nginx in the Docker Compose runtime.

## Application Metrics

SignalCart API exposes metrics for:

- HTTP request count by method, route, and status code
- HTTP request duration histogram
- in-progress requests
- products created
- orders created
- completed checkouts
- checkout failures
- database readiness
- active simulation flags

## Incident Simulations

The lab validates observability through controlled incident scenarios:

1. API latency spike
2. API error rate spike
3. PostgreSQL readiness failure
4. Nginx endpoint failure
5. Load test behavior under k6

Each incident follows an evidence-driven workflow:

1. Hypothesis
2. Experiment
3. Metric observed
4. Alert expected
5. Evidence captured
6. Diagnosis
7. Recovery
8. Lesson learned

## Evidence and Runbooks

Operational evidence is stored under:

```text
validation/
assets/screenshots/
```

Runbooks and troubleshooting notes are stored under:

```text
runbooks/
troubleshooting/
```

The goal is to make every operational claim verifiable through commands, metrics, dashboards, alerts, screenshots, and recovery notes.

## Repository Layout

```text
signalcart-observability-lab/
├── app/
├── docker/
├── dashboards/
├── alerts/
├── load-tests/
├── scripts/
├── tests/
├── docs/
├── runbooks/
├── troubleshooting/
├── assets/
├── validation/
├── migrations/
└── notes/
```

## Current Progress

- Phase 00: Host baseline and tooling preparation — completed
- Phase 01: Repository structure and documentation baseline — completed
- Phase 02: SignalCart API baseline — completed
- Phase 03: PostgreSQL, SQLAlchemy, and Alembic — completed
- Phase 04: Metrics instrumentation — completed
- Phase 05: Docker Compose runtime with Nginx — completed
- Phase 06: Prometheus and exporters — completed


## License

MIT License.

## Prometheus Jobs

Prometheus collects from these jobs:

- `prometheus`
- `signalcart-api`
- `node-exporter`
- `cadvisor`
- `postgres-exporter`
- `blackbox-nginx`

Prometheus is available locally at:

```text
http://127.0.0.1:9090
```

Prometheus target health is available at:

```text
http://127.0.0.1:9090/targets
```
