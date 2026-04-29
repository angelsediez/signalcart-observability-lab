from decimal import Decimal

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price > 0", name="ck_products_price_positive"),
        CheckConstraint("stock >= 0", name="ck_products_stock_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)

    order_items = relationship("OrderItem", back_populates="product")
