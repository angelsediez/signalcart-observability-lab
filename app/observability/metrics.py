from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from starlette.responses import Response


HTTP_REQUESTS_TOTAL = Counter(
    "signalcart_http_requests_total",
    "Total HTTP requests handled by SignalCart API.",
    labelnames=["method", "route", "status_code"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "signalcart_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    labelnames=["method", "route", "status_code"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 10.0),
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "signalcart_http_requests_in_progress",
    "Current HTTP requests being handled by SignalCart API.",
)

PRODUCTS_CREATED_TOTAL = Counter(
    "signalcart_products_created_total",
    "Total products created through SignalCart API.",
)

ORDERS_CREATED_TOTAL = Counter(
    "signalcart_orders_created_total",
    "Total orders created through SignalCart API.",
)

CHECKOUTS_COMPLETED_TOTAL = Counter(
    "signalcart_checkouts_completed_total",
    "Total successful checkouts completed through SignalCart API.",
)

CHECKOUT_FAILURES_TOTAL = Counter(
    "signalcart_checkout_failures_total",
    "Total checkout failures through SignalCart API.",
)

DATABASE_READY = Gauge(
    "signalcart_database_ready",
    "Database readiness status for SignalCart API. 1 means ready, 0 means not ready.",
)

SIMULATION_ACTIVE = Gauge(
    "signalcart_simulation_active",
    "Simulation flag state. 1 means active, 0 means inactive.",
    labelnames=["simulation"],
)

SIMULATION_NAMES = (
    "latency_spike",
    "error_spike",
    "db_readiness_failure",
)


def initialize_metrics() -> None:
    DATABASE_READY.set(0)

    for simulation_name in SIMULATION_NAMES:
        SIMULATION_ACTIVE.labels(simulation=simulation_name).set(0)


def set_database_ready(is_ready: bool) -> None:
    DATABASE_READY.set(1 if is_ready else 0)


def set_simulation_state(simulation_state: dict[str, bool]) -> None:
    for simulation_name in SIMULATION_NAMES:
        SIMULATION_ACTIVE.labels(simulation=simulation_name).set(
            1 if simulation_state.get(simulation_name, False) else 0
        )


def metrics_response() -> Response:
    return Response(
        content=generate_latest(),
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )
