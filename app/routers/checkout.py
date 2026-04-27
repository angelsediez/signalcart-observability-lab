from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.store import get_store
from app.schemas.catalog import CheckoutRequest, CheckoutResponse
from app.store import InMemoryStore

router = APIRouter(tags=["checkout"])


@router.post("/checkout", response_model=CheckoutResponse)
async def checkout(
    request: CheckoutRequest,
    store: InMemoryStore = Depends(get_store),
) -> CheckoutResponse:
    try:
        return store.checkout_order(request.order_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
