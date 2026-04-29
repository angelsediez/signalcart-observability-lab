from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.dependencies.database import get_db
from app.models import Order, Product
from app.schemas.catalog import CheckoutRequest, CheckoutResponse

router = APIRouter(tags=["checkout"])


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(
    request: CheckoutRequest,
    db: Session = Depends(get_db),
) -> CheckoutResponse:
    order = db.scalar(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == request.order_id)
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"order_id {request.order_id} does not exist",
        )

    if order.status == "checked_out":
        return CheckoutResponse(
            order_id=order.id,
            status=order.status,
            total=float(order.total),
            message="order was already checked out",
        )

    product_ids = [item.product_id for item in order.items]

    products = db.scalars(
        select(Product)
        .where(Product.id.in_(product_ids))
        .with_for_update()
    ).all()

    products_by_id = {product.id: product for product in products}

    for item in order.items:
        product = products_by_id[item.product_id]

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"product_id {item.product_id} does not have enough stock",
            )

    for item in order.items:
        product = products_by_id[item.product_id]
        product.stock -= item.quantity

    order.status = "checked_out"

    db.commit()

    return CheckoutResponse(
        order_id=order.id,
        status=order.status,
        total=float(order.total),
        message="checkout completed",
    )
