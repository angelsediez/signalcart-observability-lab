#!/usr/bin/env bash
set -euo pipefail

PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:9090}"

echo "== Prometheus target health =="
echo "PROMETHEUS_URL=${PROMETHEUS_URL}"
echo

curl -fsS "${PROMETHEUS_URL}/api/v1/targets" \
  | jq -r '
      .data.activeTargets[]
      | [
          .labels.job,
          .labels.instance,
          .health,
          (.lastError // "")
        ]
      | @tsv
    ' \
  | sort
