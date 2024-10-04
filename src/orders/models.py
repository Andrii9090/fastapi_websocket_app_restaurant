import enum
from typing import List

from database.base import Base

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship


class OrderStatus(enum.Enum):
    created = 'created'
    pending = 'pending'
    completed = 'completed'


def get_total_price(context):
    return context.get_current_parameters()['price'] * context.get_current_parameters()['quantity']


class Order(Base):
    __tablename__ = 'orders'

    name: Mapped[str] = mapped_column(nullable=False)
    order_products: Mapped[List["OrderProduct"]] = relationship(back_populates="order", lazy="selectin")
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.created)

    def __repr__(self):
        return f'<Order {self.id} {self.name}>'

    def __str__(self):
        return f'<Order {self.id} {self.name}>'


class OrderProduct(Base):
    __tablename__ = 'order_products'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))
    product: Mapped["Product"] = relationship(lazy="joined")
    price: Mapped[float] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    total_price: Mapped[float] = mapped_column(nullable=False, default=get_total_price, onupdate=get_total_price)

    order: Mapped["Order"] = relationship(back_populates="order_products")

    def __repr__(self):
        return f'<OrderProduct {self.id} {self.product.name}>'

    def __str__(self):
        return f'<OrderProduct {self.id} {self.order_id} {self.product_id}>'
