#!/usr/bin/env bash
set -euo pipefail

ALERT_NAME="${1:?alert name required}"
EXPECTED_STATE="${2:-firing}"
PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:9090}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-90}"
SLEEP_SECONDS="${SLEEP_SECONDS:-2}"

echo "Waiting for Prometheus alert ${ALERT_NAME} state=${EXPECTED_STATE}"

for attempt in $(seq 1 "${MAX_ATTEMPTS}"); do
  if curl -fsS "${PROMETHEUS_URL}/api/v1/alerts" \
    | jq -e \
      --arg alert_name "${ALERT_NAME}" \
      --arg expected_state "${EXPECTED_STATE}" \
      '.data.alerts
       | map(select(.labels.alertname == $alert_name and .state == $expected_state))
       | length > 0' >/dev/null; then
    echo "Alert ${ALERT_NAME} reached state ${EXPECTED_STATE}."
    exit 0
  fi

  echo "Attempt ${attempt}/${MAX_ATTEMPTS}: alert not in expected state yet."
  sleep "${SLEEP_SECONDS}"
done

echo "Alert ${ALERT_NAME} did not reach state ${EXPECTED_STATE} in time." >&2
exit 1
