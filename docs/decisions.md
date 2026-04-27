# Technical Decisions

This file records important technical decisions for SignalCart Observability Lab.

## Decision 001: Use SignalCart Observability Lab as the project name

**Status:** accepted

**Reason:**

The name communicates the purpose of the project: a small cart/checkout service used to generate observable signals.

## Decision 002: Keep the lab local-first

**Status:** accepted

**Reason:**

The lab is designed to run on a local Ubuntu homelab machine with Docker Compose.

This keeps the environment reproducible, inspectable, and easy to reset.

## Decision 003: Use k6 as the primary load testing tool

**Status:** accepted

**Reason:**

k6 supports scripted, repeatable load scenarios and controlled incident experiments.

This makes it suitable for validating metrics, dashboards, alert behavior, and recovery.

## Decision 004: Use Blackbox Exporter for synthetic monitoring

**Status:** accepted

**Reason:**

Blackbox Exporter validates the endpoint exposed through Nginx from an external perspective.

This complements internal application metrics from the API and exporters.

## Decision 005: Treat Nginx as the user-facing entrypoint

**Status:** accepted

**Reason:**

Nginx gives the lab a realistic HTTP entrypoint for synthetic checks, reverse proxy behavior, and endpoint availability validation.

## Decision 006: Disable simulation endpoints by default

**Status:** accepted

**Reason:**

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

**Status:** accepted

**Reason:**

Alert validation is based on visible evidence from Prometheus, Alertmanager, Grafana, command outputs, screenshots, and recovery checks.
