#!/usr/bin/env bash
set -euo pipefail

ALERTMANAGER_URL="${ALERTMANAGER_URL:-http://127.0.0.1:9093}"

echo "== Alertmanager status =="
curl -fsS "${ALERTMANAGER_URL}/api/v2/status" | jq .

echo
echo "== Alertmanager alerts =="
curl -fsS "${ALERTMANAGER_URL}/api/v2/alerts" \
  | jq -r '
      .[]
      | [
          .labels.alertname,
          (.labels.severity // ""),
          (.labels.service // ""),
          .status.state
        ]
      | @tsv
    ' \
  | sort
