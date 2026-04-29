from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.dependencies.database import get_db
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=HealthResponse)
def live(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


@router.get("/ready", response_model=ReadinessResponse)
def ready(
    request: Request,
    settings: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
) -> ReadinessResponse:
    if request.app.state.simulation_state.get("db_readiness_failure", False):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "service": settings.app_name,
                "dependencies": {
                    "database": "simulated_failure",
                },
            },
        )

    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "not_ready",
                "service": settings.app_name,
                "dependencies": {
                    "database": "unreachable",
                },
            },
        ) from exc

    return ReadinessResponse(
        status="ready",
        service=settings.app_name,
        dependencies={
            "database": "ok",
        },
    )
