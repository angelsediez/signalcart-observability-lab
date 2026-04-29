from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.money import to_money
from app.dependencies.database import get_db
from app.models import Product
from app.observability.metrics import PRODUCTS_CREATED_TOTAL
from app.schemas.catalog import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)) -> list[ProductRead]:
    products = db.scalars(select(Product).order_by(Product.id)).all()
    return [ProductRead.model_validate(product) for product in products]


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
) -> ProductRead:
    created = Product(
        name=product.name,
        price=to_money(product.price),
        stock=product.stock,
    )

    db.add(created)
    db.commit()
    db.refresh(created)

    PRODUCTS_CREATED_TOTAL.inc()

    return ProductRead.model_validate(created)
