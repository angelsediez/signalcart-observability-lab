import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.core.config import get_settings
from app.db import SessionLocal
from app.main import create_app
from app.models import Order, OrderItem, Product


def clear_database() -> None:
    with SessionLocal() as session:
        session.execute(delete(OrderItem))
        session.execute(delete(Order))
        session.execute(delete(Product))
        session.commit()


@pytest.fixture(autouse=True)
def clean_database():
    clear_database()
    yield
    clear_database()


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SIMULATION_MODE", raising=False)
    monkeypatch.delenv("SIMULATION_TOKEN", raising=False)
    get_settings.cache_clear()

    app = create_app()

    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
