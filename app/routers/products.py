from fastapi import APIRouter, Depends, status

from app.dependencies.store import get_store
from app.schemas.catalog import ProductCreate, ProductRead
from app.store import InMemoryStore

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
async def list_products(store: InMemoryStore = Depends(get_store)) -> list[ProductRead]:
    return store.list_products()


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    store: InMemoryStore = Depends(get_store),
) -> ProductRead:
    return store.create_product(product)
