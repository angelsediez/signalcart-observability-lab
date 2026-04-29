from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


def test_simulation_endpoints_are_disabled_by_default(client):
    response = client.post("/lab/simulations/latency-spike")

    assert response.status_code == 404
    assert response.json()["detail"] == "simulation endpoints are disabled"


def test_simulation_endpoint_requires_token_when_enabled(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        response = client.post("/lab/simulations/error-spike")

    assert response.status_code == 403
    assert response.json()["detail"] == "invalid simulation token"

    get_settings.cache_clear()


def test_simulation_endpoint_can_enable_and_recover_with_valid_token(monkeypatch):
    monkeypatch.setenv("SIMULATION_MODE", "true")
    monkeypatch.setenv("SIMULATION_TOKEN", "secret-token")
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as client:
        enable_response = client.post(
            "/lab/simulations/latency-spike",
            headers={"X-Simulation-Token": "secret-token"},
        )

        recover_response = client.post(
            "/lab/simulations/recover",
            headers={"X-Simulation-Token": "secret-token"},
        )

    assert enable_response.status_code == 200
    assert enable_response.json()["simulation_state"]["latency_spike"] is True

    assert recover_response.status_code == 200
    assert recover_response.json()["simulation_state"]["latency_spike"] is False
    assert recover_response.json()["simulation_state"]["error_spike"] is False
    assert recover_response.json()["simulation_state"]["db_readiness_failure"] is False

    get_settings.cache_clear()


def test_db_readiness_failure_simulation_changes_ready_endpoint(monkeypatch):
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

    assert simulation_response.status_code == 200
    assert readiness_response.status_code == 503
    assert readiness_response.json()["detail"]["dependencies"]["database"] == "simulated_failure"

    get_settings.cache_clear()
