from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.store import get_store
from app.schemas.catalog import OrderCreate, OrderRead
from app.store import InMemoryStore

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[OrderRead])
async def list_orders(store: InMemoryStore = Depends(get_store)) -> list[OrderRead]:
    return store.list_orders()


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    store: InMemoryStore = Depends(get_store),
) -> OrderRead:
    try:
        return store.create_order(order)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
