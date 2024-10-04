from typing import List

from sqlalchemy import update, select
from sqlalchemy.orm import load_only

from core.interfaces.SQLRepository import SQLRepository
from orders.models import OrderProduct
from orders.schemas import OrderDbSchema, OrderSchema, OrderCreateProduct, OrderUpdateProduct
from products.models import Product
from products.repositories import ProductRepository


class SQLOrderRepository(SQLRepository):

    def __init__(self, session, model):
        super().__init__(session, model)

    async def create(self, order: OrderDbSchema):
        new_order = self.model(name=order.name, user_id=order.user_id)
        product_repository = ProductRepository(self.session)
        for product in order.order_products:
            product_db = await product_repository.get_by_id(product.product_id)
            if product is not None:
                new_order.order_products.append(
                    OrderProduct(product_id=product_db.id, price=product_db.price, quantity=product.quantity))

        self.session.add(new_order)
        await self.session.commit()
        await self.session.refresh(new_order)
        return new_order

    async def create_order_products(self, order_products: List[OrderUpdateProduct]):
        new_order_products = []
        product_repository = ProductRepository(self.session)
        for product in order_products:
            product_db = await product_repository.get_by_id(product.product_id)
            if product is not None:
                new_order_products.append(
                    OrderProduct(product_id=product_db.id, price=product_db.price, quantity=product.quantity))

        self.session.add_all(new_order_products)
        await self.session.commit()

    async def update_order_products(self, order_products: List[OrderUpdateProduct]):
        for product in order_products:
            await self.session.execute(
                update(OrderProduct).where(OrderProduct.id == product.id).values(
                    quantity=product.quantity,
                    total_price=OrderProduct.price * product.quantity
                )
            )

        await self.session.commit()

    async def get_all(self, limit, offset, where=None, order_by=None):
        if order_by is None:
            order_by = self.model.id
        if where is None:
            result = await self.session.execute(
                select(self.model).limit(limit).offset(offset).order_by(
                    order_by.desc()))

            print(result)
        else:
            result = await self.session.execute(
                select(OrderProduct).where(where).limit(limit).offset(offset).order_by(order_by))
        return result.scalars().all()