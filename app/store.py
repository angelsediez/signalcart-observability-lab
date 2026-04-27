from app.schemas.catalog import (
    CheckoutResponse,
    OrderCreate,
    OrderRead,
    ProductCreate,
    ProductRead,
)


class InMemoryStore:
    """Temporary in-memory store.

    PostgreSQL will replace this in the database phase. Keeping this store small
    lets us validate the API surface before adding database complexity.
    """

    def __init__(self) -> None:
        self.products: dict[int, ProductRead] = {}
        self.orders: dict[int, OrderRead] = {}
        self._next_product_id = 1
        self._next_order_id = 1

    def list_products(self) -> list[ProductRead]:
        return list(self.products.values())

    def create_product(self, product: ProductCreate) -> ProductRead:
        product_id = self._next_product_id
        self._next_product_id += 1

        created = ProductRead(id=product_id, **product.model_dump())
        self.products[product_id] = created
        return created

    def list_orders(self) -> list[OrderRead]:
        return list(self.orders.values())

    def create_order(self, order: OrderCreate) -> OrderRead:
        if not order.items:
            raise ValueError("order must contain at least one item")

        total = 0.0

        for item in order.items:
            product = self.products.get(item.product_id)

            if product is None:
                raise ValueError(f"product_id {item.product_id} does not exist")

            if product.stock < item.quantity:
                raise ValueError(f"product_id {item.product_id} does not have enough stock")

            total += product.price * item.quantity

        order_id = self._next_order_id
        self._next_order_id += 1

        created = OrderRead(
            id=order_id,
            items=order.items,
            status="created",
            total=round(total, 2),
        )

        self.orders[order_id] = created
        return created

    def checkout_order(self, order_id: int) -> CheckoutResponse:
        order = self.orders.get(order_id)

        if order is None:
            raise ValueError(f"order_id {order_id} does not exist")

        if order.status == "checked_out":
            return CheckoutResponse(
                order_id=order.id,
                status=order.status,
                total=order.total,
                message="order was already checked out",
            )

        for item in order.items:
            product = self.products[item.product_id]

            if product.stock < item.quantity:
                raise ValueError(f"product_id {item.product_id} does not have enough stock")

        for item in order.items:
            product = self.products[item.product_id]
            self.products[item.product_id] = product.model_copy(
                update={"stock": product.stock - item.quantity}
            )

        checked_out = order.model_copy(update={"status": "checked_out"})
        self.orders[order_id] = checked_out

        return CheckoutResponse(
            order_id=checked_out.id,
            status=checked_out.status,
            total=checked_out.total,
            message="checkout completed",
        )
