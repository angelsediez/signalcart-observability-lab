# Technical Decisions

This file records important technical decisions for SignalCart Observability Lab.

## Decision 001: Use SignalCart Observability Lab as the project name

Status: accepted

Reason:

The name communicates the purpose of the project: a small cart/checkout service used to generate observable signals.

## Decision 002: Keep the lab local-first

Status: accepted

Reason:

The lab is designed to run on a local Ubuntu homelab machine with Docker Compose.

This keeps the environment reproducible, inspectable, and easy to reset.

## Decision 003: Use k6 as the primary load testing tool

Status: accepted

Reason:

k6 supports scripted, repeatable, local HTTP load testing using JavaScript scenarios, checks, and thresholds.

This makes it suitable for validating metrics, dashboards, alert behavior, and recovery.

## Decision 004: Use Blackbox Exporter for synthetic monitoring

Status: accepted

Reason:

Blackbox Exporter validates the endpoint exposed through Nginx from an external perspective.

This complements internal application metrics from the API and exporters.

## Decision 005: Treat Nginx as the user-facing entrypoint

Status: accepted

Reason:

Nginx gives the lab a realistic HTTP entrypoint for API traffic, health checks, metrics access, and synthetic monitoring.

## Decision 006: Disable simulation endpoints by default

Status: accepted

Reason:

Incident simulation endpoints should only be available during intentional lab exercises.

They work only when:

```env
SIMULATION_MODE=true
```

They also require:

```env
SIMULATION_TOKEN
```

## Decision 007: Validate alerts with local operational evidence

Status: accepted

Reason:

Alert validation is based on visible evidence from Prometheus, Alertmanager, Grafana, command outputs, screenshots, and recovery checks.

## Decision 008: Use PostgreSQL as the service datastore

Status: accepted

Reason:

PostgreSQL gives the lab a realistic relational datastore for persistence, readiness checks, migrations, and database monitoring.

## Decision 009: Use SQLAlchemy ORM for application persistence

Status: accepted

Reason:

SQLAlchemy ORM provides a clear Python data access layer with models, sessions, transactions, and testable database interactions.

## Decision 010: Use Alembic for database migrations

Status: accepted

Reason:

Alembic makes schema changes explicit, versioned, reviewable, and repeatable.

## Decision 011: Keep liveness independent from database readiness

Status: accepted

Reason:

`/health/live` confirms that the API process is alive.

`/health/ready` confirms that the API can use required dependencies such as PostgreSQL.

## Decision 012: Expose Prometheus metrics from the application

Status: accepted

Reason:

SignalCart API exposes application metrics directly through `/metrics` so API behavior can be validated before adding the metrics collection layer.

## Decision 013: Use low-cardinality metric labels

Status: accepted

Reason:

HTTP metrics use method, route template, and status code labels.

The API does not use raw URLs, query strings, product IDs, order IDs, or user-provided values as labels.

## Decision 014: Use RED-style HTTP metrics for API behavior

Status: accepted

Reason:

Request rate, errors, and duration provide a clear operational view of API behavior during normal traffic, load testing, and incident simulations.

## Decision 015: Run SignalCart with Docker Compose

Status: accepted

Reason:

Docker Compose provides a reproducible local runtime for the API, PostgreSQL, and Nginx.

The Compose file documents services, networks, volumes, health checks, and runtime configuration.

## Decision 016: Use Nginx as the HTTP entrypoint

Status: accepted

Reason:

Nginx gives the lab a realistic HTTP entrypoint for API traffic, health checks, metrics access, and synthetic monitoring.

## Decision 017: Run the API container as a non-root user

Status: accepted

Reason:

The API image creates and uses a dedicated `signalcart` user.

This reduces unnecessary privilege inside the application container.

## Decision 018: Use Prometheus for metrics collection

Status: accepted

Reason:

Prometheus collects application and exporter metrics through scrape jobs and provides a queryable time-series layer for operational validation.

## Decision 019: Use exporters for host, container, database, and synthetic signals

Status: accepted

Reason:

Node Exporter, cAdvisor, PostgreSQL Exporter, and Blackbox Exporter expose operational signals that the application does not provide by itself.

## Decision 020: Validate targets before building dashboards and alerts

Status: accepted

Reason:

Target validation confirms that metrics are being collected correctly before visualization and alerting are configured.

## Decision 021: Provision Grafana datasource and dashboards as code

Status: accepted

Reason:

Grafana datasource and dashboard definitions are stored in the repository so the visualization layer can be recreated from versioned files.

## Decision 022: Build focused dashboards for operational questions

Status: accepted

Reason:

The dashboards are grouped by service overview, API RED metrics, infrastructure signals, PostgreSQL behavior, and synthetic checks.

This keeps each dashboard focused and useful for troubleshooting.

## Decision 023: Store Prometheus alert rules as code

Status: accepted

Reason:

Alert rules are stored in versioned YAML files under `alerts/` so they can be reviewed, validated, and reproduced.

## Decision 024: Use Alertmanager for local alert validation

Status: accepted

Reason:

Alertmanager provides local alert grouping, deduplication, UI validation, and API validation without requiring external notification integrations.

## Decision 025: Require runbook annotations on alerts

Status: accepted

Reason:

Each alert includes a `runbook_url` annotation so alert evidence points to an operational starting point.

## Decision 026: Validate the alert pipeline with a controlled synthetic failure

Status: accepted

Reason:

Stopping Nginx temporarily validates the path from Blackbox Exporter to Prometheus alert evaluation and Alertmanager delivery.

## Decision 027: Use k6 for local load testing

Status: accepted

Reason:

k6 provides scripted, repeatable, local HTTP load testing using JavaScript scenarios, checks, and thresholds.

## Decision 028: Use smoke and baseline load profiles for normal validation

Status: accepted

Reason:

Smoke load confirms that the scripted workflow is healthy.

Baseline load generates enough traffic for Prometheus and Grafana evidence while keeping the local machine stable.

## Decision 029: Validate normal load by checking metrics and alert stability

Status: accepted

Reason:

A successful load test should increase request and checkout metrics while keeping error rate acceptable and alerts stable.


## Decision 030: Validate observability with controlled incident simulations

Status: accepted

Reason:

Controlled incidents prove that metrics, dashboards, alerts, and runbooks can be used together during realistic operational conditions.

## Decision 031: Capture before, during, and after recovery evidence

Status: accepted

Reason:

Incident evidence is more useful when it shows the complete operational timeline instead of only the failure state.

## Decision 032: Keep incident simulation local and token-protected

Status: accepted

Reason:

Simulation endpoints are intended for lab validation and require explicit runtime configuration plus a local token.
