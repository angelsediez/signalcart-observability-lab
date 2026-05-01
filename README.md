# SignalCart Observability Lab

SignalCart Observability Lab is a local-first observability homelab for practicing practical SRE operations with a small FastAPI checkout/cart service.

The lab demonstrates how to instrument, monitor, visualize, validate alerts, generate controlled load, troubleshoot, and recover a service using a metrics-driven observability workflow.

## What This Lab Demonstrates

- API health and readiness checks
- PostgreSQL-backed persistence
- SQLAlchemy data access
- Alembic database migrations
- pytest-based validation
- Prometheus-compatible application metrics
- Prometheus metrics collection
- Prometheus target validation
- Grafana dashboard provisioning
- Alertmanager alert validation
- k6 load testing evidence
- Nginx reverse proxy validation
- Docker Compose runtime validation
- Host metrics with Node Exporter
- Container metrics with cAdvisor
- PostgreSQL metrics with PostgreSQL Exporter
- Synthetic endpoint checks with Blackbox Exporter
- Controlled incident simulations
- Runbook-driven troubleshooting
- Recovery validation
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

Simulation endpoints are disabled by default and only work when:

```env
SIMULATION_MODE=true
SIMULATION_TOKEN=<local-token>
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

## Metrics Collection and Visualization Workflow

```text
SignalCart API /metrics  ----\
PostgreSQL Exporter       ----\
Node Exporter             ----- Prometheus ---- Grafana
cAdvisor                  ----/       |
Blackbox Exporter         ---/        v
        |                         Alertmanager
        v
Nginx /health/ready synthetic check
```

Prometheus collects metrics from the application and exporters. Grafana visualizes the collected metrics through provisioned dashboards. Alertmanager validates alert delivery locally. Blackbox Exporter validates the Nginx-exposed readiness endpoint from the perspective of a synthetic HTTP check.

Local service URLs:

- Nginx entrypoint: `http://127.0.0.1:8080`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`
- Alertmanager: `http://127.0.0.1:9093`
- Prometheus targets: `http://127.0.0.1:9090/targets`

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

## Prometheus Jobs

Prometheus collects from these jobs:

- `prometheus`
- `signalcart-api`
- `node-exporter`
- `cadvisor`
- `postgres-exporter`
- `blackbox-nginx`

## Grafana Dashboards

Grafana dashboards are provisioned from versioned JSON files.

Provisioned dashboards:

- SignalCart Overview
- API RED Metrics
- Infrastructure and Container Metrics
- PostgreSQL Metrics
- Synthetic Checks

Dashboard files are stored under `dashboards/`.

Grafana provisioning files are stored under `docker/grafana/provisioning/`.

## Alerting

Prometheus alert rules are stored under `alerts/`.

Alertmanager validates alert routing locally through UI and API evidence.

Implemented alert categories:

- API availability
- API error rate
- API latency
- database readiness
- PostgreSQL availability
- host saturation
- container restarts
- Nginx synthetic probe failure

## Load Testing

k6 load tests are stored under `load-tests/`.

Load test evidence is stored under `validation/load-tests/`.

Implemented profiles:

- `load-tests/smoke.js`
- `load-tests/baseline.js`
- `load-tests/stress.js`

The normal validation path uses smoke and baseline load. The stress profile is short and controlled for manual exploration.

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

The goal is to make every operational claim verifiable through commands, metrics, target status, dashboards, alerts, screenshots, and recovery notes.

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
- Phase 07: Grafana dashboards — completed
- Phase 08: Alertmanager and alert rules — completed
- Phase 09: k6 load testing and performance evidence — completed

## License

MIT License.
