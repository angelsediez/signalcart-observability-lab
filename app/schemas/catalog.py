from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OrderItem(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: list[OrderItem]


class OrderRead(BaseModel):
    id: int
    items: list[OrderItem]
    status: str
    total: float


class CheckoutRequest(BaseModel):
    order_id: int = Field(gt=0)


class CheckoutResponse(BaseModel):
    order_id: int
    status: str
    total: float
    message: str
