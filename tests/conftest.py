import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import create_app


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SIMULATION_MODE", raising=False)
    monkeypatch.delenv("SIMULATION_TOKEN", raising=False)
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
