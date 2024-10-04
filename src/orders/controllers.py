from typing import List

from core.http_response import CustomResponse
from orders.models import OrderStatus
from orders.repositories import SQLOrderRepository
from orders.schemas import CreateOrderSchema, OrderDbSchema, OrderSchema, OrderUpdateSchema, OrderCreateProduct, \
    OrderProduct, OrderUpdateProduct


class OrderController:
    def __init__(self, order_repository):
        self.order_repository = order_repository

    async def get_by_id(self, order_id: int):
        order = await self.order_repository.get_by_id(order_id)
        if order is None:
            return CustomResponse.error('Order not found')
        return CustomResponse.ok(OrderSchema.from_orm(order).dict())

    async def get_all(self, limit: int = 100, offset: int = 0, where: object = None, order_by: object = None):
        orders = await self.order_repository.get_all(limit, offset, where, order_by)
        print(orders[0])
        if orders is None:
            return CustomResponse.error('Orders not found')
        return CustomResponse.ok([OrderSchema.from_orm(order).dict() for order in orders])

    async def create(self, order: CreateOrderSchema, user_id: int):
        new_order_schema = OrderDbSchema(**order.dict(), user_id=user_id)
        new_order = await self.order_repository.create(new_order_schema)
        if new_order is None:
            return CustomResponse.error('Order not created')
        return CustomResponse.ok(OrderSchema.from_orm(new_order).json())

    async def update_order_status(self, order_id: int, status: OrderStatus):
        updated_order = await self.order_repository.update(order_id, OrderUpdateSchema(status=status))
        if updated_order is None:
            return CustomResponse.error('Order not updated')
        return CustomResponse.ok()

    async def add_order_product(self, order_id: int, products: List[OrderCreateProduct]):
        order = await self.order_repository.get_by_id(order_id)
        order_schema = OrderSchema.from_orm(order)
        new_products = []
        existed_product = []
        if order is None:
            return CustomResponse.error('Order not found')

        for product in products:
            order_product = list(filter(lambda p: p.product_id == product.product_id, order_schema.order_products))
            if len(order_product) == 0:
                new_products.append(OrderUpdateProduct(
                    order_id=order_id,
                    product_id=product.product_id,
                    price=product.price,
                    quantity=product.quantity
                ))
            else:
                order_product[0].quantity += product.quantity
                existed_product.append(order_product[0])

        if len(new_products) > 0:
            await self.order_repository.create_order_products(new_products)

        if len(existed_product) > 0:
            await self.order_repository.update_order_products(existed_product)

        return CustomResponse.ok()
