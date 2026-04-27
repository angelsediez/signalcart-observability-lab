#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8000}"

echo "== SignalCart API smoke test =="
echo "BASE_URL=${BASE_URL}"

echo
echo "## Liveness"
curl -fsS "${BASE_URL}/health/live" | jq .

echo
echo "## Readiness"
curl -fsS "${BASE_URL}/health/ready" | jq .

echo
echo "## Version"
curl -fsS "${BASE_URL}/version" | jq .

echo
echo "## Create product"
product_response="$(
  curl -fsS \
    -X POST "${BASE_URL}/products" \
    -H "Content-Type: application/json" \
    -d '{"name":"Demo Keyboard","price":49.99,"stock":10}'
)"
echo "${product_response}" | jq .

product_id="$(echo "${product_response}" | jq -r '.id')"

echo
echo "## Create order"
order_payload="$(jq -n --argjson product_id "${product_id}" '{items:[{product_id:$product_id,quantity:2}]}')"

order_response="$(
  curl -fsS \
    -X POST "${BASE_URL}/orders" \
    -H "Content-Type: application/json" \
    -d "${order_payload}"
)"
echo "${order_response}" | jq .

order_id="$(echo "${order_response}" | jq -r '.id')"

echo
echo "## Checkout"
checkout_payload="$(jq -n --argjson order_id "${order_id}" '{order_id:$order_id}')"

curl -fsS \
  -X POST "${BASE_URL}/checkout" \
  -H "Content-Type: application/json" \
  -d "${checkout_payload}" | jq .

echo
echo "Smoke test completed successfully."
