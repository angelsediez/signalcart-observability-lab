from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app.core.config import Settings, get_settings
from app.observability.metrics import set_simulation_state

router = APIRouter(prefix="/lab/simulations", tags=["lab"])


def require_simulation_access(
    x_simulation_token: str | None = Header(default=None, alias="X-Simulation-Token"),
    settings: Settings = Depends(get_settings),
) -> None:
    if not settings.simulation_mode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="simulation endpoints are disabled",
        )

    if not x_simulation_token or x_simulation_token != settings.simulation_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="invalid simulation token",
        )


def get_simulation_state(request: Request) -> dict[str, bool]:
    return request.app.state.simulation_state


@router.post("/latency-spike", dependencies=[Depends(require_simulation_access)])
async def latency_spike(
    simulation_state: dict[str, bool] = Depends(get_simulation_state),
) -> dict[str, object]:
    simulation_state["latency_spike"] = True
    set_simulation_state(simulation_state)

    return {"status": "enabled", "simulation_state": simulation_state}


@router.post("/error-spike", dependencies=[Depends(require_simulation_access)])
async def error_spike(
    simulation_state: dict[str, bool] = Depends(get_simulation_state),
) -> dict[str, object]:
    simulation_state["error_spike"] = True
    set_simulation_state(simulation_state)

    return {"status": "enabled", "simulation_state": simulation_state}


@router.post("/db-readiness-failure", dependencies=[Depends(require_simulation_access)])
async def db_readiness_failure(
    simulation_state: dict[str, bool] = Depends(get_simulation_state),
) -> dict[str, object]:
    simulation_state["db_readiness_failure"] = True
    set_simulation_state(simulation_state)

    return {"status": "enabled", "simulation_state": simulation_state}


@router.post("/recover", dependencies=[Depends(require_simulation_access)])
async def recover(
    simulation_state: dict[str, bool] = Depends(get_simulation_state),
) -> dict[str, object]:
    for key in simulation_state:
        simulation_state[key] = False

    set_simulation_state(simulation_state)

    return {"status": "recovered", "simulation_state": simulation_state}
