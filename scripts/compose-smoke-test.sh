#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"

echo "== SignalCart Compose smoke test =="
echo "BASE_URL=${BASE_URL}"

bash scripts/wait-for-api.sh

BASE_URL="${BASE_URL}" bash scripts/smoke-test.sh

echo
echo "## Metrics through Nginx"
curl -fsS "${BASE_URL}/metrics" | grep -E '^(# HELP|# TYPE|signalcart_)' | head -n 80

echo
echo "Compose smoke test completed successfully."
