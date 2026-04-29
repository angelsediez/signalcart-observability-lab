import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.observability.metrics import (
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_IN_PROGRESS,
    HTTP_REQUESTS_TOTAL,
)


def should_skip_metrics(request: Request) -> bool:
    return request.url.path == "/metrics"


def get_route_template(request: Request) -> str:
    route = request.scope.get("route")
    route_path = getattr(route, "path", None)

    if route_path:
        return route_path

    return "unmatched"


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if should_skip_metrics(request):
            return await call_next(request)

        method = request.method
        status_code = "500"
        start_time = time.perf_counter()

        HTTP_REQUESTS_IN_PROGRESS.inc()

        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            return response
        finally:
            duration = time.perf_counter() - start_time
            route = get_route_template(request)

            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                route=route,
                status_code=status_code,
            ).inc()

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method,
                route=route,
                status_code=status_code,
            ).observe(duration)

            HTTP_REQUESTS_IN_PROGRESS.dec()
