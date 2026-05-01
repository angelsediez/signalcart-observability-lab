import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

export const options = {
  scenarios: {
    smoke: {
      executor: 'shared-iterations',
      vus: 1,
      iterations: 5,
      maxDuration: '1m',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
    checks: ['rate>0.99'],
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
    name: uniqueName('smoke-product'),
    price: 19.99,
    stock: 10,
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

  sleep(1);
}
