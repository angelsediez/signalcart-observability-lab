import time

from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


def create_product_order(client: TestClient) -> int:
    product_response = client.post(
        "/products",
        json={
            "name": "Incident Test Product",
            "price": 15.00,
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

    return order_response.json()["id"]


def test_simulation_endpoint_requires_token_when_runtime_mode_enabled(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        response = client.post("/lab/simulations/latency-spike")

    assert response.status_code == 403

    get_settings.cache_clear()


def test_latency_spike_slows_checkout_when_enabled(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    monkeypatch.setenv("SIMULATION_LATENCY_SECONDS", "0.05")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        order_id = create_product_order(client)

        simulation_response = client.post(
            "/lab/simulations/latency-spike",
            headers={"X-Simulation-Token": "secret-token"},
        )

        start = time.perf_counter()
        checkout_response = client.post("/checkout", json={"order_id": order_id})
        elapsed = time.perf_counter() - start

    assert simulation_response.status_code == 200
    assert checkout_response.status_code == 200
    assert elapsed >= 0.05

    get_settings.cache_clear()


def test_error_spike_returns_controlled_500_for_checkout(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    monkeypatch.setenv("SIMULATION_ERROR_STATUS_CODE", "500")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        order_id = create_product_order(client)

        simulation_response = client.post(
            "/lab/simulations/error-spike",
            headers={"X-Simulation-Token": "secret-token"},
        )

        checkout_response = client.post("/checkout", json={"order_id": order_id})

    assert simulation_response.status_code == 200
    assert checkout_response.status_code == 500
    assert checkout_response.json()["simulation"] == "error_spike"

    get_settings.cache_clear()
