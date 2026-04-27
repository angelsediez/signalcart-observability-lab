# SignalCart Observability Lab

SignalCart Observability Lab is a local-first observability homelab for practicing practical SRE operations with a small FastAPI checkout/cart service.

The lab demonstrates how to instrument, monitor, visualize, alert on, troubleshoot, and recover a service using a metrics-driven observability workflow.

## What This Lab Demonstrates

- API health and readiness checks
- Application metrics
- Prometheus scraping
- Grafana dashboards
- Alertmanager alert validation
- Synthetic monitoring with Blackbox Exporter
- Host and container monitoring
- PostgreSQL monitoring
- Load testing with k6
- Controlled incident simulations
- Runbook-driven troubleshooting
- Recovery validation
- Evidence-based incident documentation

## Service Under Observation

The application under observation is **SignalCart API**, a small checkout/cart API with products, orders, checkout, health checks, metrics, and controlled incident simulation endpoints.

The application is intentionally simple so the main focus stays on observability, SRE operations, incident response, and troubleshooting.

### Planned application endpoints

- `GET /health/live`
- `GET /health/ready`
- `GET /version`
- `GET /metrics`
- `GET /products`
- `POST /products`
- `GET /orders`
- `POST /orders`
- `POST /checkout`

### Lab simulation endpoints

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
- Prometheus
- Grafana
- Alertmanager
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
SignalCart API /metrics  ----\
PostgreSQL Exporter       ----\
Node Exporter             ----- Prometheus ---- Grafana
cAdvisor                  ----/       |
Blackbox Exporter         ---/        v
                                  Alertmanager
```

Prometheus collects metrics from the application and exporters. Grafana visualizes service and infrastructure behavior. Alertmanager is used to validate alerts during controlled incidents. Blackbox Exporter checks the endpoint exposed through Nginx from an external perspective.

## Incident Simulations

The lab validates observability through controlled incident scenarios:

- API latency spike
- API error rate spike
- PostgreSQL readiness failure
- Nginx endpoint failure
- Load test behavior under k6

Each incident follows an evidence-driven workflow:

- Hypothesis
- Experiment
- Metric observed
- Alert expected
- Evidence captured
- Diagnosis
- Recovery
- Lesson learned

## Evidence and Runbooks

Operational evidence is stored under:

- `validation/`
- `assets/screenshots/`

Runbooks and troubleshooting notes are stored under:

- `runbooks/`
- `troubleshooting/`

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
└── notes/
```

## Current Progress

- Phase 00: Host baseline and tooling preparation — completed
- Phase 01: Repository structure and documentation baseline — in progress

## Source Material Policy

Study PDFs and books are local learning sources only.

They are not copied into this repository.

The repository intentionally ignores:

- `*.pdf`
- `brain/`
- `main_sources/`

## License

MIT License.