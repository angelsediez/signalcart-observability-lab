<div align="center">

# 📡 SignalCart Observability Lab

### Local-first DevOps/SRE observability homelab for practicing metrics, dashboards, alerting, load testing, incident simulation, and recovery validation

![Status](https://img.shields.io/badge/Status-Completed_Lab-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![k6](https://img.shields.io/badge/k6-Load_Testing-7D64FF?style=for-the-badge&logo=k6&logoColor=white)

</div>

---

## 📌 Overview

**SignalCart Observability Lab** is a local DevOps/SRE homelab built around a small FastAPI checkout/cart service and a complete observability stack.

The lab demonstrates how a service is instrumented, monitored, visualized, load tested, alerted on, and recovered after controlled incidents. It is designed as a practical portfolio project for validating operational workflows with real evidence instead of static diagrams only.

The project covers:

- FastAPI service runtime with operational endpoints
- PostgreSQL persistence with SQLAlchemy and Alembic
- Prometheus-compatible application metrics
- Docker Compose orchestration
- Nginx reverse proxy entrypoint
- Prometheus metrics collection and alert rules
- Grafana dashboards provisioned as code
- Alertmanager alert routing and incident visibility
- k6 smoke and baseline load testing
- controlled latency, error, and database-readiness incident simulations
- runbooks, troubleshooting notes, screenshots, and validation artifacts

> [!IMPORTANT]
> **Lab State:** Complete local observability baseline.
> **Final Phase:** Phase 10 — incident simulation, recovery validation, screenshots, and stored evidence.

---

## 🎯 Learning Focus

This lab was built to practice operating a small service with production-style observability patterns in a reproducible local environment.

Core learning areas:

- service health and readiness validation
- API metrics instrumentation
- database-backed service operation
- Prometheus scraping and query validation
- Grafana dashboard provisioning
- Alertmanager alert routing
- synthetic endpoint checks with Blackbox Exporter
- container and host-level metrics with cAdvisor and Node Exporter
- PostgreSQL metrics with PostgreSQL Exporter
- load testing with k6
- incident detection, investigation, and recovery validation
- evidence-based documentation for DevOps/SRE workflows

---

## 🧭 Architecture at a Glance

```text
Runtime request path

user / curl / k6 -> nginx -> SignalCart API -> PostgreSQL
```

```text
Observability path

SignalCart API /metrics
Node Exporter
cAdvisor
PostgreSQL Exporter
Blackbox Exporter
        -> Prometheus -> Grafana
        -> Prometheus -> Alertmanager
```

| Domain | Components | Purpose |
| :--- | :--- | :--- |
| Application runtime | `api`, `nginx`, `postgres` | FastAPI service, reverse proxy, and database runtime |
| Metrics collection | `prometheus`, exporters, `/metrics` | Scrape and query application, infrastructure, container, database, and synthetic signals |
| Visualization | `grafana` | Provisioned dashboards for service, API RED, infrastructure, PostgreSQL, and synthetic checks |
| Alerting | `prometheus`, `alertmanager` | Rule evaluation, alert routing, and incident visibility |
| Load testing | `k6`, `load-tests/` | Smoke, baseline, and stress workflow definitions |
| Operations | `scripts/`, `runbooks/`, `troubleshooting/`, `validation/` | Incident execution, recovery guidance, and evidence capture |

---

## 🗺️ System Diagrams

### Runtime Architecture

<img src="assets/diagrams/runtime-architecture.png" width="100%" alt="SignalCart runtime architecture diagram" />

### Observability Flow

<img src="assets/diagrams/observability-flow_v2.png" width="100%" alt="SignalCart observability flow diagram" />

### Alerting and Incident Response

<img src="assets/diagrams/alerting-incident-response.png" width="100%" alt="SignalCart alerting and incident response flow diagram" />

### Load Testing Workflow

<img src="assets/diagrams/load-testing-workflow.png" width="100%" alt="SignalCart load testing workflow diagram" />

### Incident Simulation and Recovery

<img src="assets/diagrams/incident-simulation-recovery.png" width="100%" alt="SignalCart incident simulation and recovery diagram" />

---

## 🧰 Technical Stack

### Application and Data

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square)
![Alembic](https://img.shields.io/badge/Alembic-Migrations-6B7280?style=flat-square)
![pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC?style=flat-square&logo=pytest&logoColor=white)

### Runtime and Observability

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker_Compose-Orchestration-2496ED?style=flat-square&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-009639?style=flat-square&logo=nginx&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?style=flat-square&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?style=flat-square&logo=grafana&logoColor=white)
![Alertmanager](https://img.shields.io/badge/Alertmanager-Alerting-E6522C?style=flat-square)
![k6](https://img.shields.io/badge/k6-Load_Testing-7D64FF?style=flat-square&logo=k6&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-Automation-4EAA25?style=flat-square&logo=gnubash&logoColor=white)

---

## ✅ Completed Lab Phases

| Phase | Scope | Status |
| :--- | :--- | :---: |
| Phase 00 | Host baseline and tooling preparation | ✅ |
| Phase 01 | Repository structure and documentation baseline | ✅ |
| Phase 02 | SignalCart API baseline | ✅ |
| Phase 03 | PostgreSQL, SQLAlchemy, and Alembic persistence | ✅ |
| Phase 04 | Prometheus application metrics instrumentation | ✅ |
| Phase 05 | Docker Compose runtime with Nginx | ✅ |
| Phase 06 | Prometheus and exporters | ✅ |
| Phase 07 | Grafana dashboard provisioning | ✅ |
| Phase 08 | Alertmanager alerting and runbooks | ✅ |
| Phase 09 | k6 load testing and performance evidence | ✅ |
| Phase 10 | Incident simulation and recovery evidence | ✅ |

---

## 🖼️ Evidence Gallery

### 🚀 API and Database Baseline

| FastAPI health endpoints | OpenAPI docs |
| :---: | :---: |
| <img src="assets/screenshots/phase-02/P02-01-fastapi-health-endpoints.png" width="100%" alt="FastAPI health endpoints validation" /> | <img src="assets/screenshots/phase-02/P02-02-fastapi-openapi-docs.png" width="100%" alt="FastAPI OpenAPI docs" /> |

| PostgreSQL container healthy | API readiness with database OK |
| :---: | :---: |
| <img src="assets/screenshots/phase-03/P03-01-postgres-container-healthy.png" width="100%" alt="PostgreSQL container healthy" /> | <img src="assets/screenshots/phase-03/P03-04-api-readiness-db-ok.png" width="100%" alt="API readiness confirms database OK" /> |

### 📈 Metrics and Runtime Validation

| Metrics endpoint baseline | Metrics after API traffic |
| :---: | :---: |
| <img src="assets/screenshots/phase-04/P04-01-metrics-endpoint-baseline.png" width="100%" alt="Prometheus metrics endpoint baseline" /> | <img src="assets/screenshots/phase-04/P04-04-metrics-after-api-traffic.png" width="100%" alt="Metrics after API traffic" /> |

| Compose runtime up | Nginx readiness through reverse proxy |
| :---: | :---: |
| <img src="assets/screenshots/phase-05/P05-01-compose-runtime-up.png" width="100%" alt="Docker Compose runtime up" /> | <img src="assets/screenshots/phase-05/P05-02-nginx-readiness-db-ok.png" width="100%" alt="Nginx readiness database OK" /> |

### 🔥 Prometheus and Grafana

| Prometheus targets up | Exporter targets up |
| :---: | :---: |
| <img src="assets/screenshots/phase-06/P06-01-prometheus-targets-up.png" width="100%" alt="Prometheus targets up" /> | <img src="assets/screenshots/phase-06/P06-03-exporters-targets-up.png" width="100%" alt="Exporter targets up" /> |

| Grafana overview dashboard | API RED dashboard |
| :---: | :---: |
| <img src="assets/screenshots/phase-07/P07-01-grafana-overview-dashboard.png" width="100%" alt="Grafana overview dashboard" /> | <img src="assets/screenshots/phase-07/P07-02-api-red-dashboard.png" width="100%" alt="Grafana API RED dashboard" /> |

| Infrastructure dashboard | PostgreSQL dashboard |
| :---: | :---: |
| <img src="assets/screenshots/phase-07/P07-03-infrastructure-dashboard.png" width="100%" alt="Grafana infrastructure dashboard" /> | <img src="assets/screenshots/phase-07/P07-04-postgres-dashboard.png" width="100%" alt="Grafana PostgreSQL dashboard" /> |

### 🚨 Alerting and Recovery

| Prometheus rules loaded | Alertmanager UI ready |
| :---: | :---: |
| <img src="assets/screenshots/phase-08/P08-01-prometheus-rules-loaded.png" width="100%" alt="Prometheus alert rules loaded" /> | <img src="assets/screenshots/phase-08/P08-02-alertmanager-ui-ready.png" width="100%" alt="Alertmanager UI ready" /> |

| Alert firing in Prometheus | Alert resolved after recovery |
| :---: | :---: |
| <img src="assets/screenshots/phase-08/P08-03-nginx-alert-firing-prometheus.png" width="100%" alt="Nginx alert firing in Prometheus" /> | <img src="assets/screenshots/phase-08/P08-05-alert-resolved-after-recovery.png" width="100%" alt="Alert resolved after recovery" /> |

### ⚙️ Load Testing and Incident Simulation

| k6 baseline success | Prometheus request evidence after load |
| :---: | :---: |
| <img src="assets/screenshots/phase-09/P09-02-k6-baseline-success.png" width="100%" alt="k6 baseline success" /> | <img src="assets/screenshots/phase-09/P09-03-prometheus-request-rate-after-load.png" width="100%" alt="Prometheus request traffic after load" /> |

| Grafana API RED after load | Alerts stable after load |
| :---: | :---: |
| <img src="assets/screenshots/phase-09/P09-04-grafana-api-red-after-load.png" width="100%" alt="Grafana API RED after load" /> | <img src="assets/screenshots/phase-09/P09-05-alerts-stable-after-load.png" width="100%" alt="Alerts stable after normal load" /> |

| Latency spike evidence | Error spike dashboard |
| :---: | :---: |
| <img src="assets/screenshots/phase-10/P10-01-latency-spike-prometheus.png" width="100%" alt="Latency spike evidence in Prometheus" /> | <img src="assets/screenshots/phase-10/P10-02-error-spike-grafana-api-red.png" width="100%" alt="Error spike visible in Grafana API RED dashboard" /> |

| Database readiness incident | Final recovery validation |
| :---: | :---: |
| <img src="assets/screenshots/phase-10/P10-03-db-readiness-alert-prometheus.png" width="100%" alt="Database readiness alert evidence" /> | <img src="assets/screenshots/phase-10/P10-04-recovery-validation-terminal.png" width="100%" alt="Final recovery validation" /> |

<details>
<summary><strong>More phase evidence</strong></summary>

Evidence is organized by phase under:

```text
assets/screenshots/
├── phase-00/
├── phase-02/
├── phase-03/
├── phase-04/
├── phase-05/
├── phase-06/
├── phase-07/
├── phase-08/
├── phase-09/
└── phase-10/
```

Validation artifacts are stored under:

```text
validation/
├── database-baseline/
├── metrics-baseline/
├── compose-runtime/
├── prometheus-targets/
├── grafana-dashboards/
├── alerting/
├── load-tests/
└── incidents/
```

</details>

---

## 🧪 What This Lab Practices and Validates

| Area | Practiced Capability |
| :--- | :--- |
| API operations | Liveness, readiness, version, products, orders, checkout, and metrics endpoints |
| Data operations | PostgreSQL persistence, SQLAlchemy models, Alembic migrations, readiness dependency checks |
| Testing | pytest unit tests, integration checks, smoke tests, and validation artifacts |
| Container runtime | Docker Compose services, healthchecks, named volumes, local service networking |
| Reverse proxy | Nginx as the public entrypoint in front of the API |
| Metrics | Prometheus-compatible application metrics and exporter metrics |
| Dashboards | Grafana dashboards for overview, API RED, infrastructure, PostgreSQL, and synthetic checks |
| Alerting | Prometheus alert rules and Alertmanager routing |
| Synthetic checks | Blackbox Exporter readiness probing through Nginx |
| Load testing | k6 smoke and baseline workflows with summary JSON evidence |
| Incident response | controlled latency, error, and database-readiness simulations with recovery validation |
| Documentation | runbooks, troubleshooting guides, screenshots, and stored command outputs |

---

## 📂 Repository Map

```text
.
├── app/                    # FastAPI app, routers, models, db wiring, observability middleware
├── dashboards/             # Grafana dashboard JSON definitions
├── docker/                 # Dockerfile, Nginx config, Prometheus, Grafana, Alertmanager configs
├── docs/                   # Architecture, setup guide, observability model, alerting strategy, decisions
├── load-tests/             # k6 smoke, baseline, and stress scripts
├── migrations/             # Alembic migration environment and versions
├── runbooks/               # Operational runbooks for alerts and incident response
├── scripts/                # Runtime checks, Prometheus/Grafana validation, load testing, incident simulation
├── tests/                  # Unit and integration tests
├── troubleshooting/        # Debugging guides for app, Nginx, Prometheus, Grafana, alerts, and database issues
├── assets/diagrams/        # Architecture and workflow diagrams
├── assets/screenshots/     # Phase-based visual evidence
├── validation/             # Command outputs, JSON responses, test summaries, and incident evidence
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── requirements-dev.txt
```

---

## 🚀 Run Locally with Docker Compose

### 1. Create local environment file

```bash
cp .env.example .env
```

### 2. Build and start the runtime

```bash
docker compose up -d --build
```

### 3. Apply database migrations

```bash
docker compose exec -T api alembic upgrade head
```

### 4. Validate running services

```bash
docker compose ps
```

### 5. Validate API through Nginx

```bash
curl -s http://127.0.0.1:8080/health/live | jq .
curl -s http://127.0.0.1:8080/health/ready | jq .
curl -s http://127.0.0.1:8080/version | jq .
curl -s http://127.0.0.1:8080/metrics | head
```

### 6. Open local UIs

| Service | URL |
| :--- | :--- |
| SignalCart API through Nginx | `http://127.0.0.1:8080` |
| Prometheus | `http://127.0.0.1:9090` |
| Grafana | `http://127.0.0.1:3000` |
| Alertmanager | `http://127.0.0.1:9093` |

---

## 📊 Prometheus and Grafana Validation

### Validate Prometheus targets

```bash
bash scripts/check-prometheus-targets.sh
```

### Validate Grafana provisioning

```bash
bash scripts/check-grafana-provisioning.sh
```

### Useful Prometheus queries

```promql
up
```

```promql
signalcart_database_ready
```

```promql
sum by (route, status_code) (increase(signalcart_http_requests_total[30m]))
```

```promql
histogram_quantile(0.95, sum(rate(signalcart_http_request_duration_seconds_bucket[5m])) by (le))
```

---

## 🧨 Load Testing

### Run k6 smoke test

```bash
BASE_URL=http://127.0.0.1:8080 k6 run load-tests/smoke.js
```

### Run k6 baseline test

```bash
BASE_URL=http://127.0.0.1:8080 k6 run load-tests/baseline.js
```

### Run with summary export

```bash
BASE_URL=http://127.0.0.1:8080 \
k6 run --summary-export validation/load-tests/P09-k6-baseline-summary.json \
load-tests/baseline.js
```

Validation confirms:

- checks pass
- failed request rate remains zero during normal load
- p95 latency is measured
- Prometheus observes request traffic
- Grafana visualizes API RED metrics
- no unexpected firing alerts appear during normal load

---

## 🧯 Incident Simulation and Recovery

Incident simulation endpoints are protected and require local simulation mode plus a simulation token.

### Run full incident workflow

```bash
BASE_URL=http://127.0.0.1:8080 \
PROMETHEUS_URL=http://127.0.0.1:9090 \
SIMULATION_TOKEN=local-simulation-token \
bash scripts/run-incident-simulation.sh
```

The workflow validates:

- latency spike increases p95 response duration
- error spike increases 5xx error percentage
- database readiness failure changes readiness from healthy to failed
- recovery restores health endpoints
- `signalcart_database_ready` returns to `1`
- dashboards stabilize
- final firing alert count returns to `0`

---

## 🧾 Key Documentation

| Document | Purpose |
| :--- | :--- |
| [`docs/setup-guide.md`](docs/setup-guide.md) | Full local setup, runtime validation, dashboards, alerts, load tests, and incident simulation |
| [`docs/architecture.md`](docs/architecture.md) | Runtime architecture and observability stack model |
| [`docs/observability-model.md`](docs/observability-model.md) | Metrics, dashboards, alerts, synthetic checks, load testing, and incident validation model |
| [`docs/alerting-strategy.md`](docs/alerting-strategy.md) | Alert categories, validation strategy, and operational evidence model |
| [`docs/decisions.md`](docs/decisions.md) | Architecture and operational decisions |
| [`runbooks/README.md`](runbooks/README.md) | Runbook index and alert response guidance |
| [`troubleshooting/README.md`](troubleshooting/README.md) | Troubleshooting index for runtime and observability failures |
| [`validation/README.md`](validation/README.md) | Validation evidence index |
| [`assets/screenshots/README.md`](assets/screenshots/README.md) | Screenshot evidence index |

---

## 🧠 Design Decisions

- Nginx is the public HTTP entrypoint for the API.
- SignalCart API exposes Prometheus-compatible metrics at `/metrics`.
- Prometheus collects application metrics, exporter metrics, and synthetic probe results.
- Grafana is provisioned from versioned dashboard JSON files.
- Alertmanager receives routed alerts from Prometheus.
- Blackbox Exporter validates the externally exposed Nginx readiness endpoint.
- k6 is used for repeatable local smoke and baseline load testing.
- Controlled simulations are triggered through protected SignalCart API endpoints.
- Recovery validation is based on health endpoints, Prometheus queries, dashboards, alerts, and stored evidence.

---

## ✅ Lab Status

> [!IMPORTANT]
> **Status:** Complete ✅
> **Phases:** Phase 00 through Phase 10 complete.
> **Lab State:** Completed DevOps/SRE observability homelab with API runtime, PostgreSQL persistence, Nginx, Prometheus, Grafana, Alertmanager, k6 load testing, controlled incident simulations, runbooks, troubleshooting, screenshots, and validation evidence.

---

## 👤 Author

**Angel Diez**
