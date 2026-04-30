# Database Migrations

This directory contains Alembic migrations for SignalCart API.

Alembic is used to make database schema changes explicit, versioned, reviewable, and repeatable.

## Purpose

The database schema supports:

- products
- orders
- order items
- Alembic schema version tracking

## Main Files

```text
migrations/
├── env.py
├── README.md
├── script.py.mako
└── versions/
```

## Applying Migrations Locally

When running the API locally with PostgreSQL available:

```bash
alembic upgrade head
```

## Applying Migrations in Docker Compose

When running the containerized runtime:

```bash
docker compose exec -T api alembic upgrade head
```

## Checking Migration State

```bash
docker compose exec -T postgres psql -U signalcart -d signalcart -c "SELECT * FROM alembic_version;"
```

## Inspecting Tables

```bash
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\dt"
```

## Inspecting Table Schemas

```bash
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\d products"
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\d orders"
docker compose exec -T postgres psql -U signalcart -d signalcart -c "\d order_items"
```

## Migration Rules

- Do not edit an applied migration casually.
- Prefer creating a new migration for schema changes.
- Keep migrations readable.
- Keep schema changes tied to application changes.
- Validate migrations with tests and smoke checks.
- Capture migration evidence under `validation/database-baseline/` or the relevant phase directory.

## Current Schema Summary

### products

Stores product catalog data:

- `id`
- `name`
- `price`
- `stock`

### orders

Stores order headers:

- `id`
- `status`
- `total`

### order_items

Stores order line items:

- `id`
- `order_id`
- `product_id`
- `quantity`
- `unit_price`
