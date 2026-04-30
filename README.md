# SignalCart Observability Lab

SignalCart Observability Lab is a local-first observability homelab for practicing SRE operations with a small FastAPI checkout/cart service.

## What This Lab Demonstrates

- API health and readiness checks
- PostgreSQL-backed persistence with SQLAlchemy and Alembic
- Prometheus-compatible application metrics
- Prometheus metrics collection and target validation
- Grafana dashboards provisioned as code
- Nginx reverse proxy validation
- Docker Compose runtime validation
- Node Exporter, cAdvisor, PostgreSQL Exporter, and Blackbox Exporter
- k6 load testing preparation
- controlled incident simulations
- runbook-driven troubleshooting
- evidence-based operational documentation

## Service Under Observation

SignalCart API exposes products, orders, checkout, health, version, metrics, and controlled lab simulation endpoints.

Application endpoints: `GET /health/live`, `GET /health/ready`, `GET /version`, `GET /metrics`, `GET /products`, `POST /products`, `GET /orders`, `POST /orders`, `POST /checkout`.

Lab simulation endpoints: `POST /lab/simulations/latency-spike`, `POST /lab/simulations/error-spike`, `POST /lab/simulations/db-readiness-failure`, `POST /lab/simulations/recover`.

Simulation endpoints are disabled by default and require `SIMULATION_MODE=true` plus `SIMULATION_TOKEN`.

## Technologies Used

FastAPI, PostgreSQL, SQLAlchemy, Alembic, pytest, Nginx, Docker Compose, Prometheus, Grafana, prometheus-client, Node Exporter, cAdvisor, PostgreSQL Exporter, Blackbox Exporter, k6, Bash scripts, runbooks, troubleshooting docs, validation evidence, and screenshots.

## Architecture

```text
User / curl / k6 -> Nginx -> SignalCart API -> PostgreSQL
```

## Metrics Collection Workflow

```text
SignalCart API /metrics  ----\
PostgreSQL Exporter       ----\
Node Exporter             ----- Prometheus ---- Grafana
cAdvisor                  ----/
Blackbox Exporter         ---/  (probes Nginx /health/ready)
```

Prometheus: `http://127.0.0.1:9090`

Grafana: `http://127.0.0.1:3000`

Prometheus targets: `http://127.0.0.1:9090/targets`

## Grafana Dashboards

Provisioned dashboards:

- SignalCart Overview
- API RED Metrics
- Infrastructure and Container Metrics
- PostgreSQL Metrics
- Synthetic Checks

Dashboard JSON files live under `dashboards/`. Grafana provisioning files live under `docker/grafana/provisioning/`.

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


## License

MIT License.
