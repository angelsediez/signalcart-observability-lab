#!/usr/bin/env bash
set -euo pipefail

PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:9090}"

echo "== Prometheus rule groups =="
curl -fsS "${PROMETHEUS_URL}/api/v1/rules?type=alert" \
  | jq -r '
      .data.groups[]
      | .name as $group
      | .rules[]
      | [
          $group,
          .name,
          .state,
          (.labels.severity // ""),
          (.labels.service // "")
        ]
      | @tsv
    ' \
  | sort

echo
echo "== Active Prometheus alerts =="
curl -fsS "${PROMETHEUS_URL}/api/v1/alerts" \
  | jq -r '
      .data.alerts[]
      | [
          .labels.alertname,
          .state,
          (.labels.severity // ""),
          (.labels.service // "")
        ]
      | @tsv
    ' \
  | sort
