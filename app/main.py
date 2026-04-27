from fastapi import FastAPI

from app.core.config import get_settings
from app.routers import checkout, health, orders, products, simulations, version
from app.store import InMemoryStore


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="SignalCart API for the SignalCart Observability Lab.",
    )

    app.state.store = InMemoryStore()
    app.state.simulation_state = {
        "latency_spike": False,
        "error_spike": False,
        "db_readiness_failure": False,
    }

    app.include_router(health.router)
    app.include_router(version.router)
    app.include_router(products.router)
    app.include_router(orders.router)
    app.include_router(checkout.router)
    app.include_router(simulations.router)

    return app


app = create_app()
