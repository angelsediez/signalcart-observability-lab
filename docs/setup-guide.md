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
## Running SignalCart API Locally

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install development dependencies:

```bash
python -m pip install -r requirements-dev.txt
```

Run the API locally:

```bash
uvicorn app.main:app --reload
```

Validate health endpoints:

```bash
curl -s http://127.0.0.1:8000/health/live | jq .
curl -s http://127.0.0.1:8000/health/ready | jq .
```

Run the smoke test:

```bash
bash scripts/smoke-test.sh
```

Run tests:

```bash
pytest -q
```
