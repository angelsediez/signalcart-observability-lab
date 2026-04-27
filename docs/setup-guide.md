# Setup Guide

## Host Baseline

Target host:

- Ubuntu 24.04.4 LTS
- local homelab machine
- Docker Engine
- Docker Compose plugin
- k6

Phase 00 evidence is stored in:

```text
validation/host-baseline/
assets/screenshots/phase-00/
```

## Local Repository

Expected location:

`~/projects/signalcart-observability-lab`

Remote:

`git@github.com-signalcart:angelsediez/signalcart-observability-lab.git`

## Required Host Tools

- git
- curl
- jq
- make
- tree
- python3
- pip3
- Docker Engine
- Docker Compose plugin
- k6

## Environment Variables

Use `.env.example` as the template for local configuration.

```bash
cp .env.example .env
```

Simulation endpoints are disabled by default:

```env
SIMULATION_MODE=false
```

To run incident simulations during the lab, set:

```env
SIMULATION_MODE=true
SIMULATION_TOKEN=your-local-token
```

## Evidence Locations

Text evidence:

```text
validation/
```

Screenshots:

```text
assets/screenshots/
```

Runbooks:

```text
runbooks/
```

Troubleshooting notes:

```text
troubleshooting/
```

## Source Material Policy

Study PDFs and books are local learning sources only.

They are not copied into this repository.

The repository intentionally ignores:

```gitignore
*.pdf
brain/
main_sources/
```