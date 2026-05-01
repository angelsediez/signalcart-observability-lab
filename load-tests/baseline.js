import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

export const options = {
  scenarios: {
    baseline: {
      executor: 'ramping-vus',
      stages: [
        { duration: '30s', target: 3 },
        { duration: '2m', target: 5 },
        { duration: '30s', target: 0 },
      ],
      gracefulRampDown: '10s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.02'],
    http_req_duration: ['p(95)<1200'],
    checks: ['rate>0.98'],
  },
};

function jsonHeaders() {
  return {
    headers: {
      'Content-Type': 'application/json',
    },
  };
}

function uniqueName(prefix) {
  return `${prefix}-${__VU}-${__ITER}-${Date.now()}`;
}

function randomSleep() {
  sleep(Math.random() * 0.8 + 0.2);
}

export default function () {
  const live = http.get(`${BASE_URL}/health/live`, {
    tags: { name: 'GET /health/live' },
  });

  check(live, {
    'live status is 200': (r) => r.status === 200,
  });

  const ready = http.get(`${BASE_URL}/health/ready`, {
    tags: { name: 'GET /health/ready' },
  });

  check(ready, {
    'ready status is 200': (r) => r.status === 200,
    'ready database is ok': (r) => r.json('dependencies.database') === 'ok',
  });

  const version = http.get(`${BASE_URL}/version`, {
    tags: { name: 'GET /version' },
  });

  check(version, {
    'version status is 200': (r) => r.status === 200,
  });

  const productPayload = JSON.stringify({
    name: uniqueName('baseline-product'),
    price: 24.99,
    stock: 20,
  });

  const product = http.post(`${BASE_URL}/products`, productPayload, {
    ...jsonHeaders(),
    tags: { name: 'POST /products' },
  });

  check(product, {
    'product created': (r) => r.status === 201,
    'product has id': (r) => Number(r.json('id')) > 0,
  });

  const productId = product.json('id');

  const orderPayload = JSON.stringify({
    items: [
      {
        product_id: productId,
        quantity: 1,
      },
    ],
  });

  const order = http.post(`${BASE_URL}/orders`, orderPayload, {
    ...jsonHeaders(),
    tags: { name: 'POST /orders' },
  });

  check(order, {
    'order created': (r) => r.status === 201,
    'order has id': (r) => Number(r.json('id')) > 0,
  });

  const orderId = order.json('id');

  const checkoutPayload = JSON.stringify({
    order_id: orderId,
  });

  const checkout = http.post(`${BASE_URL}/checkout`, checkoutPayload, {
    ...jsonHeaders(),
    tags: { name: 'POST /checkout' },
  });

  check(checkout, {
    'checkout completed': (r) => r.status === 200,
    'checkout status checked_out': (r) => r.json('status') === 'checked_out',
  });

  randomSleep();
}
