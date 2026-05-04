import asyncio
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import get_settings


class IncidentSimulationMiddleware(BaseHTTPMiddleware):
    """Applies controlled lab incident behavior when simulation flags are active."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        simulation_state = getattr(request.app.state, "simulation_state", {})
        settings = get_settings()

        is_checkout = request.method == "POST" and request.url.path == "/checkout"

        if is_checkout and simulation_state.get("latency_spike", False):
            await asyncio.sleep(settings.simulation_latency_seconds)

        if is_checkout and simulation_state.get("error_spike", False):
            return JSONResponse(
                status_code=settings.simulation_error_status_code,
                content={
                    "detail": "simulated checkout error spike",
                    "simulation": "error_spike",
                },
            )

        return await call_next(request)
