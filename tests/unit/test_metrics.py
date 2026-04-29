from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


def get_metric_value(metrics_text: str, metric_name: str) -> float:
    for line in metrics_text.splitlines():
        if line.startswith(f"{metric_name} "):
            return float(line.split()[-1])

    raise AssertionError(f"metric {metric_name} not found")


def test_metrics_endpoint_returns_prometheus_text(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]

    body = response.text

    assert "signalcart_http_requests_total" in body
    assert "signalcart_http_request_duration_seconds" in body
    assert "signalcart_http_requests_in_progress" in body
    assert "signalcart_products_created_total" in body
    assert "signalcart_orders_created_total" in body
    assert "signalcart_checkouts_completed_total" in body
    assert "signalcart_checkout_failures_total" in body
    assert "signalcart_database_ready" in body
    assert "signalcart_simulation_active" in body


def test_domain_counters_increase_after_product_order_and_checkout(client):
    before = client.get("/metrics").text

    before_products = get_metric_value(before, "signalcart_products_created_total")
    before_orders = get_metric_value(before, "signalcart_orders_created_total")
    before_checkouts = get_metric_value(before, "signalcart_checkouts_completed_total")

    product_response = client.post(
        "/products",
        json={
            "name": "Metrics Mouse",
            "price": 29.99,
            "stock": 5,
        },
    )
    assert product_response.status_code == 201

    product_id = product_response.json()["id"]

    order_response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1,
                }
            ]
        },
    )
    assert order_response.status_code == 201

    order_id = order_response.json()["id"]

    checkout_response = client.post(
        "/checkout",
        json={"order_id": order_id},
    )
    assert checkout_response.status_code == 200

    after = client.get("/metrics").text

    assert get_metric_value(after, "signalcart_products_created_total") >= before_products + 1
    assert get_metric_value(after, "signalcart_orders_created_total") >= before_orders + 1
    assert get_metric_value(after, "signalcart_checkouts_completed_total") >= before_checkouts + 1


def test_checkout_failure_counter_increases_after_failed_checkout(client):
    before = client.get("/metrics").text
    before_failures = get_metric_value(before, "signalcart_checkout_failures_total")

    response = client.post("/checkout", json={"order_id": 999999})

    assert response.status_code == 400

    after = client.get("/metrics").text

    assert get_metric_value(after, "signalcart_checkout_failures_total") >= before_failures + 1


def test_database_ready_metric_is_one_after_successful_readiness_check(client):
    readiness_response = client.get("/health/ready")

    assert readiness_response.status_code == 200

    metrics = client.get("/metrics").text

    assert get_metric_value(metrics, "signalcart_database_ready") == 1


def test_database_ready_metric_is_zero_during_simulated_readiness_failure(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        simulation_response = client.post(
            "/lab/simulations/db-readiness-failure",
            headers={"X-Simulation-Token": "secret-token"},
        )
        readiness_response = client.get("/health/ready")
        metrics = client.get("/metrics").text

    assert simulation_response.status_code == 200
    assert readiness_response.status_code == 503
    assert get_metric_value(metrics, "signalcart_database_ready") == 0

    get_settings.cache_clear()


def test_simulation_metrics_reflect_active_flags(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        response = client.post(
            "/lab/simulations/error-spike",
            headers={"X-Simulation-Token": "secret-token"},
        )
        metrics = client.get("/metrics").text

    assert response.status_code == 200
    assert 'signalcart_simulation_active{simulation="error_spike"} 1.0' in metrics

    get_settings.cache_clear()
