#!/usr/bin/env bash
set -euo pipefail

GRAFANA_URL="${GRAFANA_URL:-http://127.0.0.1:3000}"
GRAFANA_USER="${GRAFANA_USER:-admin}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-admin}"

echo "== Grafana health =="
curl -fsS -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" \
  "${GRAFANA_URL}/api/health" | jq .

echo
echo "== Grafana Prometheus datasource =="
curl -fsS -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" \
  "${GRAFANA_URL}/api/datasources/name/Prometheus" | jq '{name, uid, type, url, isDefault}'

echo
echo "== Provisioned SignalCart dashboards =="
curl -fsS -u "${GRAFANA_USER}:${GRAFANA_PASSWORD}" \
  "${GRAFANA_URL}/api/search?query=SignalCart" \
  | jq -r '.[] | [.title, .uid, .type, .folderTitle] | @tsv'
