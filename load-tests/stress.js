import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.BASE_URL || 'http://127.0.0.1:8080';

export const options = {
  scenarios: {
    short_stress: {
      executor: 'ramping-vus',
      stages: [
        { duration: '20s', target: 8 },
        { duration: '40s', target: 8 },
        { duration: '20s', target: 0 },
      ],
      gracefulRampDown: '10s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<2000'],
    checks: ['rate>0.95'],
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
  const ready = http.get(`${BASE_URL}/health/ready`, {
    tags: { name: 'GET /health/ready' },
  });

  check(ready, {
    'ready status is 200': (r) => r.status === 200,
  });

  const product = http.post(
    `${BASE_URL}/products`,
    JSON.stringify({
      name: uniqueName('stress-product'),
      price: 9.99,
      stock: 10,
    }),
    {
      ...jsonHeaders(),
      tags: { name: 'POST /products' },
    }
  );

  check(product, {
    'product created': (r) => r.status === 201,
  });

  const productId = product.json('id');

  const order = http.post(
    `${BASE_URL}/orders`,
    JSON.stringify({
      items: [
        {
          product_id: productId,
          quantity: 1,
        },
      ],
    }),
    {
      ...jsonHeaders(),
      tags: { name: 'POST /orders' },
    }
  );

  check(order, {
    'order created': (r) => r.status === 201,
  });

  const orderId = order.json('id');

  const checkout = http.post(
    `${BASE_URL}/checkout`,
    JSON.stringify({
      order_id: orderId,
    }),
    {
      ...jsonHeaders(),
      tags: { name: 'POST /checkout' },
    }
  );

  check(checkout, {
    'checkout completed': (r) => r.status === 200,
  });

  sleep(0.2);
}
