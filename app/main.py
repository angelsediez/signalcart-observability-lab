from fastapi import FastAPI

from app.core.config import get_settings
from app.observability.incident_middleware import IncidentSimulationMiddleware
from app.observability.metrics import initialize_metrics, set_simulation_state
from app.observability.middleware import MetricsMiddleware
from app.routers import checkout, health, metrics, orders, products, simulations, version


def create_app() -> FastAPI:
    settings = get_settings()

    initialize_metrics()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="SignalCart API for the SignalCart Observability Lab.",
    )

    app.state.simulation_state = {
        "latency_spike": False,
        "error_spike": False,
        "db_readiness_failure": False,
    }

    set_simulation_state(app.state.simulation_state)

    app.add_middleware(IncidentSimulationMiddleware)
    app.add_middleware(MetricsMiddleware)

    app.include_router(health.router)
    app.include_router(metrics.router)
    app.include_router(version.router)
    app.include_router(products.router)
    app.include_router(orders.router)
    app.include_router(checkout.router)
    app.include_router(simulations.router)

    return app


app = create_app()
