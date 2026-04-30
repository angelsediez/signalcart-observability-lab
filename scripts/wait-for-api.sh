#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-30}"
SLEEP_SECONDS="${SLEEP_SECONDS:-2}"

echo "Waiting for SignalCart API at ${BASE_URL}"

for attempt in $(seq 1 "${MAX_ATTEMPTS}"); do
  if curl -fsS "${BASE_URL}/health/ready" >/dev/null; then
    echo "SignalCart API is ready."
    exit 0
  fi

  echo "Attempt ${attempt}/${MAX_ATTEMPTS}: API not ready yet."
  sleep "${SLEEP_SECONDS}"
done

echo "SignalCart API did not become ready in time." >&2
exit 1
