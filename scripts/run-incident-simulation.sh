#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8080}"
PROMETHEUS_URL="${PROMETHEUS_URL:-http://127.0.0.1:9090}"
SIMULATION_TOKEN="${SIMULATION_TOKEN:-local-simulation-token}"
EVIDENCE_DIR="${EVIDENCE_DIR:-validation/incidents}"

mkdir -p "${EVIDENCE_DIR}"

simulation_header=(
  -H "X-Simulation-Token: ${SIMULATION_TOKEN}"
)

json_header=(
  -H "Content-Type: application/json"
)

query_prometheus() {
  local query="$1"
  local output_file="$2"

  curl -fsS -G "${PROMETHEUS_URL}/api/v1/query" \
    --data-urlencode "query=${query}" \
    | jq . \
    | tee "${output_file}" >/dev/null
}

capture_alerts() {
  local output_file="$1"

  curl -fsS "${PROMETHEUS_URL}/api/v1/alerts" \
    | jq . \
    | tee "${output_file}" >/dev/null
}

recover_simulations() {
  curl -fsS \
    -X POST "${BASE_URL}/lab/simulations/recover" \
    "${simulation_header[@]}" \
    | jq . >/dev/null
}

create_product_order() {
  local prefix="$1"

  local product_response
  product_response="$(
    curl -fsS \
      -X POST "${BASE_URL}/products" \
      "${json_header[@]}" \
      -d "{\"name\":\"${prefix}-product-$(date +%s%N)\",\"price\":19.99,\"stock\":20}"
  )"

  local product_id
  product_id="$(echo "${product_response}" | jq -r '.id')"

  local order_response
  order_response="$(
    curl -fsS \
      -X POST "${BASE_URL}/orders" \
      "${json_header[@]}" \
      -d "{\"items\":[{\"product_id\":${product_id},\"quantity\":1}]}"
  )"

  echo "${order_response}" | jq -r '.id'
}

checkout_once() {
  local order_id="$1"
  local output_file="$2"

  curl -sS \
    -X POST "${BASE_URL}/checkout" \
    "${json_header[@]}" \
    -d "{\"order_id\":${order_id}}" \
    | jq . \
    | tee "${output_file}" >/dev/null
}

generate_checkout_traffic() {
  local label="$1"
  local seconds="$2"
  local output_file="$3"

  local end_time
  end_time=$((SECONDS + seconds))

  echo "Generating ${label} checkout traffic for ${seconds}s" | tee "${output_file}"

  while [ "${SECONDS}" -lt "${end_time}" ]; do
    local order_id
    order_id="$(create_product_order "${label}")"

    local status_code
    status_code="$(
      curl -sS \
        -o /dev/null \
        -w "%{http_code}" \
        -X POST "${BASE_URL}/checkout" \
        "${json_header[@]}" \
        -d "{\"order_id\":${order_id}}"
    )"

    echo "$(date --iso-8601=seconds) ${label} checkout_status=${status_code}" | tee -a "${output_file}"
    sleep 0.2
  done
}

echo "== SignalCart incident simulation validation =="
echo "BASE_URL=${BASE_URL}"
echo "PROMETHEUS_URL=${PROMETHEUS_URL}"
echo "EVIDENCE_DIR=${EVIDENCE_DIR}"

echo
echo "## Runtime readiness"
curl -fsS "${BASE_URL}/health/ready" | jq . | tee "${EVIDENCE_DIR}/P10-runtime-ready-before-incidents.json" >/dev/null

echo
echo "## Simulation protection check"
{
  echo "No token status:"
  curl -sS -o /dev/null -w "%{http_code}\n" -X POST "${BASE_URL}/lab/simulations/latency-spike"

  echo "Invalid token status:"
  curl -sS -o /dev/null -w "%{http_code}\n" \
    -X POST "${BASE_URL}/lab/simulations/latency-spike" \
    -H "X-Simulation-Token: invalid-token"
} | tee "${EVIDENCE_DIR}/P10-simulation-protection.txt"

recover_simulations

echo
echo "## Latency spike before"
query_prometheus \
  'histogram_quantile(0.95, sum by (le) (rate(signalcart_http_request_duration_seconds_bucket[5m])))' \
  "${EVIDENCE_DIR}/P10-latency-spike-before.json"

curl -fsS \
  -X POST "${BASE_URL}/lab/simulations/latency-spike" \
  "${simulation_header[@]}" \
  | jq . \
  | tee "${EVIDENCE_DIR}/P10-latency-simulation-enabled.json" >/dev/null

generate_checkout_traffic "latency-spike" 75 "${EVIDENCE_DIR}/P10-latency-spike-traffic.txt"

sleep 20

query_prometheus \
  'histogram_quantile(0.95, sum by (le) (rate(signalcart_http_request_duration_seconds_bucket[5m])))' \
  "${EVIDENCE_DIR}/P10-latency-spike-during.json"

cp "${EVIDENCE_DIR}/P10-latency-spike-during.json" \
  "${EVIDENCE_DIR}/P10-prometheus-latency-query-during.json"

recover_simulations

sleep 20

generate_checkout_traffic "latency-recovery" 20 "${EVIDENCE_DIR}/P10-latency-recovery-traffic.txt"

sleep 20

query_prometheus \
  'histogram_quantile(0.95, sum by (le) (rate(signalcart_http_request_duration_seconds_bucket[5m])))' \
  "${EVIDENCE_DIR}/P10-latency-spike-after-recovery.json"

echo
echo "## Error spike before"
query_prometheus \
  '100 * sum(rate(signalcart_http_requests_total{status_code=~"5.."}[5m])) / clamp_min(sum(rate(signalcart_http_requests_total[5m])), 0.001)' \
  "${EVIDENCE_DIR}/P10-error-spike-before.json"

curl -fsS \
  -X POST "${BASE_URL}/lab/simulations/error-spike" \
  "${simulation_header[@]}" \
  | jq . \
  | tee "${EVIDENCE_DIR}/P10-error-simulation-enabled.json" >/dev/null

generate_checkout_traffic "error-spike" 75 "${EVIDENCE_DIR}/P10-error-spike-traffic.txt"

sleep 20

query_prometheus \
  '100 * sum(rate(signalcart_http_requests_total{status_code=~"5.."}[5m])) / clamp_min(sum(rate(signalcart_http_requests_total[5m])), 0.001)' \
  "${EVIDENCE_DIR}/P10-error-spike-during.json"

cp "${EVIDENCE_DIR}/P10-error-spike-during.json" \
  "${EVIDENCE_DIR}/P10-prometheus-error-rate-query-during.json"

capture_alerts "${EVIDENCE_DIR}/P10-prometheus-alerts-during-error-spike.json"

recover_simulations

sleep 20

generate_checkout_traffic "error-recovery" 20 "${EVIDENCE_DIR}/P10-error-recovery-traffic.txt"

sleep 20

query_prometheus \
  '100 * sum(rate(signalcart_http_requests_total{status_code=~"5.."}[5m])) / clamp_min(sum(rate(signalcart_http_requests_total[5m])), 0.001)' \
  "${EVIDENCE_DIR}/P10-error-spike-after-recovery.json"

echo
echo "## Database readiness before"
curl -fsS "${BASE_URL}/health/ready" \
  | jq . \
  | tee "${EVIDENCE_DIR}/P10-db-readiness-before-health.json" >/dev/null

query_prometheus \
  'signalcart_database_ready' \
  "${EVIDENCE_DIR}/P10-db-readiness-before.json"

curl -fsS \
  -X POST "${BASE_URL}/lab/simulations/db-readiness-failure" \
  "${simulation_header[@]}" \
  | jq . \
  | tee "${EVIDENCE_DIR}/P10-db-readiness-simulation-enabled.json" >/dev/null

curl -sS "${BASE_URL}/health/ready" \
  | jq . \
  | tee "${EVIDENCE_DIR}/P10-db-readiness-during-health.json" >/dev/null || true

sleep 20

query_prometheus \
  'signalcart_database_ready' \
  "${EVIDENCE_DIR}/P10-db-readiness-during.json"

cp "${EVIDENCE_DIR}/P10-db-readiness-during.json" \
  "${EVIDENCE_DIR}/P10-prometheus-database-ready-query-during.json"

capture_alerts "${EVIDENCE_DIR}/P10-prometheus-alerts-during-incidents.json"

echo "Waiting for DatabaseReadinessFailing to reach firing or pending evidence"
for attempt in $(seq 1 75); do
  capture_alerts "${EVIDENCE_DIR}/P10-prometheus-alerts-db-readiness-check.json"

  if jq -e '
    .data.alerts
    | map(select(.labels.alertname == "DatabaseReadinessFailing" and (.state == "firing" or .state == "pending")))
    | length > 0
  ' "${EVIDENCE_DIR}/P10-prometheus-alerts-db-readiness-check.json" >/dev/null; then
    echo "DatabaseReadinessFailing is visible in Prometheus."
    break
  fi

  echo "Attempt ${attempt}/75: DatabaseReadinessFailing not visible yet."
  sleep 2
done | tee "${EVIDENCE_DIR}/P10-db-readiness-alert-wait.txt"

recover_simulations

sleep 5

curl -fsS "${BASE_URL}/health/ready" \
  | jq . \
  | tee "${EVIDENCE_DIR}/P10-db-readiness-after-recovery-health.json" >/dev/null

sleep 20

query_prometheus \
  'signalcart_database_ready' \
  "${EVIDENCE_DIR}/P10-db-readiness-after-recovery.json"

capture_alerts "${EVIDENCE_DIR}/P10-prometheus-alerts-after-recovery.json"

echo
echo "## Final summary"
{
  echo "== Incident validation summary =="
  echo
  echo "Latency evidence:"
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-latency-spike-before.json" | sed 's/^/before_p95=/'
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-latency-spike-during.json" | sed 's/^/during_p95=/'
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-latency-spike-after-recovery.json" | sed 's/^/after_p95=/'

  echo
  echo "Error evidence:"
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-error-spike-before.json" | sed 's/^/before_error_percent=/'
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-error-spike-during.json" | sed 's/^/during_error_percent=/'
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-error-spike-after-recovery.json" | sed 's/^/after_error_percent=/'

  echo
  echo "Database readiness evidence:"
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-db-readiness-before.json" | sed 's/^/before_db_ready=/'
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-db-readiness-during.json" | sed 's/^/during_db_ready=/'
  jq -r '.data.result[]?.value[1] // "no result"' "${EVIDENCE_DIR}/P10-db-readiness-after-recovery.json" | sed 's/^/after_db_ready=/'

  echo
  echo "Alerts after recovery:"
  jq -r '
    .data.alerts[]
    | select(.state == "firing")
    | [.labels.alertname, (.labels.severity // ""), (.labels.service // "")]
    | @tsv
  ' "${EVIDENCE_DIR}/P10-prometheus-alerts-after-recovery.json" || true

  echo
  echo "Firing alert count after recovery:"
  jq '[.data.alerts[] | select(.state == "firing")] | length' \
    "${EVIDENCE_DIR}/P10-prometheus-alerts-after-recovery.json"
} | tee "${EVIDENCE_DIR}/P10-incident-validation-summary.txt"

echo "Incident simulation validation completed."
