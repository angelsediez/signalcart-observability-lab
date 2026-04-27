def test_liveness_endpoint_returns_ok(client):
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "SignalCart API"


def test_readiness_endpoint_returns_ready_without_database_dependency_yet(client):
    response = client.get("/health/ready")

    assert response.status_code == 200
    body = response.json()

    assert body["status"] == "ready"
    assert body["dependencies"]["database"] == "not_configured"


def test_version_endpoint_returns_service_metadata(client):
    response = client.get("/version")

    assert response.status_code == 200
    body = response.json()

    assert body["service"] == "SignalCart API"
    assert body["version"] == "0.1.0"
    assert body["environment"] == "local"
