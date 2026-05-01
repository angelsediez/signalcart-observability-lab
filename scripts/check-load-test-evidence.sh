#!/usr/bin/env bash
set -euo pipefail

PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:9090}"

echo "== SignalCart load test evidence check =="

echo
echo "## Request rate"
curl -fsS -G "${PROMETHEUS_URL}/api/v1/query" \
  --data-urlencode 'query=sum(rate(signalcart_http_requests_total[5m]))' \
  | jq .

echo
echo "## p95 latency"
curl -fsS -G "${PROMETHEUS_URL}/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.95, sum by (le) (rate(signalcart_http_request_duration_seconds_bucket[5m])))' \
  | jq .

echo
echo "## error percentage"
curl -fsS -G "${PROMETHEUS_URL}/api/v1/query" \
  --data-urlencode 'query=100 * sum(rate(signalcart_http_requests_total{status_code=~"5.."}[5m])) / clamp_min(sum(rate(signalcart_http_requests_total[5m])), 0.001)' \
  | jq .

echo
echo "## active alerts"
curl -fsS "${PROMETHEUS_URL}/api/v1/alerts" \
  | jq .
