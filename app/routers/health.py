from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=HealthResponse)
async def live(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


@router.get("/ready", response_model=ReadinessResponse)
async def ready(settings: Settings = Depends(get_settings)) -> ReadinessResponse:
    return ReadinessResponse(
        status="ready",
        service=settings.app_name,
        dependencies={
            "database": "not_configured",
        },
    )
