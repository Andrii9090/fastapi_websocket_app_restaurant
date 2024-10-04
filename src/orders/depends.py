from fastapi import Depends

from core.interfaces.abstract_repository import AbstractRepository
from database.connect import async_session_generator
from orders.controllers import OrderController
from orders.models import Order
from orders.repositories import SQLOrderRepository


def get_order_repository(session=Depends(async_session_generator)) -> AbstractRepository:
    return SQLOrderRepository(session, Order)


def get_order_controller(order_repository: AbstractRepository = Depends(get_order_repository)) -> OrderController:
    return OrderController(order_repository)
