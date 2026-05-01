# Technical Decisions

This file records important technical decisions for SignalCart Observability Lab.

## Decision 001: Use SignalCart Observability Lab as the project name

Status: accepted

Reason: the name communicates a small cart/checkout service used to generate observable signals.

## Decision 002: Keep the lab local-first

Status: accepted

Reason: the lab runs on a local Ubuntu homelab machine with Docker Compose, which keeps the environment reproducible, inspectable, and easy to reset.

## Decision 003: Use k6 as the primary load testing tool

Status: accepted

Reason: k6 supports scripted, repeatable load scenarios and controlled incident experiments.

## Decision 004: Use Blackbox Exporter for synthetic monitoring

Status: accepted

Reason: Blackbox Exporter validates the endpoint exposed through Nginx from an external perspective.

## Decision 005: Treat Nginx as the user-facing entrypoint

Status: accepted

Reason: Nginx gives the lab a realistic HTTP entrypoint for API traffic, health checks, metrics access, and synthetic monitoring.

## Decision 006: Disable simulation endpoints by default

Status: accepted

Reason: incident simulation endpoints should only be available during intentional lab exercises and require `SIMULATION_MODE=true` plus `SIMULATION_TOKEN`.

## Decision 007: Validate alerts with local operational evidence

Status: accepted

Reason: alert validation is based on visible evidence from Prometheus, Alertmanager, Grafana, command outputs, screenshots, and recovery checks.

## Decision 008: Use PostgreSQL as the service datastore

Status: accepted

Reason: PostgreSQL gives the lab a realistic relational datastore for persistence, readiness checks, migrations, and database monitoring.

## Decision 009: Use SQLAlchemy ORM for application persistence

Status: accepted

Reason: SQLAlchemy ORM provides a clear Python data access layer with models, sessions, transactions, and testable database interactions.

## Decision 010: Use Alembic for database migrations

Status: accepted

Reason: Alembic makes schema changes explicit, versioned, reviewable, and repeatable.

## Decision 011: Keep liveness independent from database readiness

Status: accepted

Reason: `/health/live` confirms the API process is alive, while `/health/ready` confirms required dependencies such as PostgreSQL are usable.

## Decision 012: Expose Prometheus metrics from the application

Status: accepted

Reason: SignalCart API exposes application metrics directly through `/metrics` so API behavior can be validated before collection and visualization.

## Decision 013: Use low-cardinality metric labels

Status: accepted

Reason: HTTP metrics use method, route template, and status code labels, avoiding raw URLs, query strings, product IDs, order IDs, or user-provided values.

## Decision 014: Use RED-style HTTP metrics for API behavior

Status: accepted

Reason: request rate, errors, and duration provide a clear operational view of API behavior.

## Decision 015: Run SignalCart with Docker Compose

Status: accepted

Reason: Docker Compose provides a reproducible local runtime for the API, PostgreSQL, and Nginx.

## Decision 016: Use Nginx as the HTTP entrypoint

Status: accepted

Reason: Nginx gives the lab a realistic entrypoint for health checks, metrics access, and synthetic monitoring.

## Decision 017: Run the API container as a non-root user

Status: accepted

Reason: the API image creates and uses a dedicated `signalcart` user.

## Decision 018: Use Prometheus for metrics collection

Status: accepted

Reason: Prometheus collects application and exporter metrics through scrape jobs and provides a queryable time-series layer.

## Decision 019: Use exporters for host, container, database, and synthetic signals

Status: accepted

Reason: Node Exporter, cAdvisor, PostgreSQL Exporter, and Blackbox Exporter expose operational signals the application does not provide by itself.

## Decision 020: Validate targets before building dashboards and alerts

Status: accepted

Reason: target validation confirms that metrics are being collected correctly before visualization and alerting are configured.

## Decision 021: Provision Grafana datasource and dashboards as code

Status: accepted

Reason: Grafana datasource and dashboard definitions are stored in the repository and can be recreated from versioned files.

## Decision 022: Build focused dashboards for operational questions

Status: accepted

Reason: dashboards are grouped by service overview, API RED metrics, infrastructure signals, PostgreSQL behavior, and synthetic checks.

## Decision 023: Store Prometheus alert rules as code

Status: accepted

Reason: alert rules are stored in versioned YAML files under `alerts/` so they can be reviewed, validated, and reproduced.

## Decision 024: Use Alertmanager for local alert validation

Status: accepted

Reason: Alertmanager provides local alert grouping, deduplication, UI validation, and API validation without external notification integrations.

## Decision 025: Require runbook annotations on alerts

Status: accepted

Reason: each alert includes a `runbook_url` annotation so alert evidence points to an operational starting point.

## Decision 026: Validate the alert pipeline with a controlled synthetic failure

Status: accepted

Reason: stopping Nginx temporarily validates the path from Blackbox Exporter to Prometheus alert evaluation and Alertmanager delivery.
