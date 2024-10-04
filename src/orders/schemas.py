from typing import List

from pydantic import BaseModel, Field

from orders.models import OrderStatus
from products.schemas import ProductSchema


class OrderCreateProduct(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, default=1)

    class Config:
        from_attributes = True


class OrderUpdateProduct(OrderCreateProduct):
    order_id: int


class OrderProduct(OrderCreateProduct):
    id: int
    total_price: float
    product: ProductSchema


class CreateOrderSchema(BaseModel):
    name: str
    order_products: List[OrderCreateProduct]

    class Config:
        from_attributes = True


class OrderDbSchema(CreateOrderSchema):
    user_id: int

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: int
    name: str
    status: OrderStatus
    order_products: List[OrderProduct]

    class Config:
        from_attributes = True
        exclude_unset = True


class OrderUpdateSchema(BaseModel):
    status: OrderStatus

    class Config:
        from_attributes = True
