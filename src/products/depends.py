from fastapi import Depends

from core.interfaces.abstract_repository import AbstractRepository
from database.connect import async_session_generator
from products.controllers import ProductController
from products.repositories import ProductRepository


async def get_product_repository(session=Depends(async_session_generator)) -> AbstractRepository:
    return ProductRepository(session)


async def get_product_controller(
        product_repository: AbstractRepository = Depends(get_product_repository)) -> ProductController:
    return ProductController(product_repository)

