from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.money import to_money
from app.dependencies.database import get_db
from app.models import Order, OrderItem as OrderItemModel, Product
from app.observability.metrics import ORDERS_CREATED_TOTAL
from app.schemas.catalog import OrderCreate, OrderItem, OrderRead

router = APIRouter(prefix="/orders", tags=["orders"])


def order_to_read(order: Order) -> OrderRead:
    return OrderRead(
        id=order.id,
        items=[
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
            )
            for item in order.items
        ],
        status=order.status,
        total=float(order.total),
    )


@router.get("", response_model=list[OrderRead])
def list_orders(db: Session = Depends(get_db)) -> list[OrderRead]:
    orders = db.scalars(
        select(Order)
        .options(selectinload(Order.items))
        .order_by(Order.id)
    ).all()

    return [order_to_read(order) for order in orders]


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderRead:
    if not order.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order must contain at least one item",
        )

    product_ids = {item.product_id for item in order.items}

    products = db.scalars(
        select(Product).where(Product.id.in_(product_ids))
    ).all()

    products_by_id = {product.id: product for product in products}

    total = Decimal("0.00")

    created = Order(status="created", total=Decimal("0.00"))

    for item in order.items:
        product = products_by_id.get(item.product_id)

        if product is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"product_id {item.product_id} does not exist",
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"product_id {item.product_id} does not have enough stock",
            )

        unit_price = to_money(product.price)
        total += unit_price * item.quantity

        created.items.append(
            OrderItemModel(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=unit_price,
            )
        )

    created.total = to_money(total)

    db.add(created)
    db.commit()

    ORDERS_CREATED_TOTAL.inc()

    return order_to_read(created)
