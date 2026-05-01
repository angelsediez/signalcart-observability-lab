# SignalCart Observability Lab

SignalCart Observability Lab is a local-first observability homelab for practicing practical SRE operations with a small FastAPI checkout/cart service.

The lab demonstrates how to instrument, monitor, visualize, validate alerts, troubleshoot, and recover a service using a metrics-driven observability workflow.

## What This Lab Demonstrates

- API health and readiness checks
- PostgreSQL-backed persistence
- SQLAlchemy data access
- Alembic database migrations
- pytest-based validation
- Prometheus-compatible application metrics
- Prometheus metrics collection and target validation
- Grafana dashboard provisioning
- Alertmanager alert validation
- Nginx reverse proxy validation
- Docker Compose runtime validation
- Host metrics with Node Exporter
- Container metrics with cAdvisor
- PostgreSQL metrics with PostgreSQL Exporter
- Synthetic endpoint checks with Blackbox Exporter
- Controlled incident simulations
- Runbook-driven troubleshooting
- Evidence-based operational documentation

## Service Under Observation

The application under observation is **SignalCart API**, a small checkout/cart API with products, orders, checkout, health checks, metrics, and controlled incident simulation endpoints.

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

Simulation endpoints are disabled by default and require `SIMULATION_MODE=true` plus `SIMULATION_TOKEN`.

## Technologies Used

FastAPI, PostgreSQL, SQLAlchemy, Alembic, pytest, Nginx, Docker Compose, Prometheus, Grafana, Alertmanager, prometheus-client, Node Exporter, cAdvisor, PostgreSQL Exporter, Blackbox Exporter, k6, Bash scripts, runbooks, troubleshooting docs, validation evidence, and screenshots.

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

## Metrics and Alerting Workflow

```text
SignalCart API /metrics  ----\
PostgreSQL Exporter       ----\
Node Exporter             ----- Prometheus ---- Grafana
cAdvisor                  ----/       |
Blackbox Exporter         ---/        v
                                  Alertmanager
```

Prometheus collects metrics from the application and exporters. Grafana visualizes the collected metrics through provisioned dashboards. Alertmanager receives alerts from Prometheus and provides local alert validation through UI and API evidence.

Local endpoints:

- Nginx: `http://127.0.0.1:8080`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`
- Alertmanager: `http://127.0.0.1:9093`

## Prometheus Jobs

- `prometheus`
- `signalcart-api`
- `node-exporter`
- `cadvisor`
- `postgres-exporter`
- `blackbox-nginx`

## Grafana Dashboards

Provisioned dashboards:

- SignalCart Overview
- API RED Metrics
- Infrastructure and Container Metrics
- PostgreSQL Metrics
- Synthetic Checks

## Alert Rules

Alert rule files live under `alerts/` and cover API availability, API errors, API latency, database readiness, PostgreSQL availability, host saturation, container restart signals, and Nginx synthetic probe failure.

Every alert includes severity, service, category, summary, description, and runbook URL.

## Evidence and Runbooks

Operational evidence is stored under `validation/` and `assets/screenshots/`.

Runbooks and troubleshooting notes are stored under `runbooks/` and `troubleshooting/`.

## Current Progress

- Phase 00: Host baseline and tooling preparation — completed
- Phase 01: Repository structure and documentation baseline — completed
- Phase 02: SignalCart API baseline — completed
- Phase 03: PostgreSQL, SQLAlchemy, and Alembic — completed
- Phase 04: Metrics instrumentation — completed
- Phase 05: Docker Compose runtime with Nginx — completed
- Phase 06: Prometheus and exporters — completed
- Phase 07: Grafana dashboards — completed
- Phase 08: Alertmanager and alert rules — completed


## License

MIT License.
