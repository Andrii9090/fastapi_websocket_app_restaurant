from core.http_response import CustomResponse
from core.interfaces.abstract_repository import AbstractRepository
from products.schemas import ProductSchema, ProductUpdateSchema, ProductCreateSchema, ProductSoftDeleteSchema


class ProductController:
    def __init__(self, product_repository: AbstractRepository):
        self.repository = product_repository

    async def get_all(self, limit, offset, where: object = None):
        products = await self.repository.get_all(limit, offset, where)
        if products is None:
            return CustomResponse.error('Products not found')
        return CustomResponse.ok([ProductSchema.from_orm(product).dict() for product in products])

    async def get_product(self, product_id):
        product = await self.repository.get_by_id(product_id)
        if product is None:
            return CustomResponse.error('Product not found')
        return CustomResponse.ok(ProductSchema.from_orm(product).dict())

    async def create(self, product, user_id):
        new_product = ProductCreateSchema(**product.dict(), user_id=user_id)
        created_product = await self.repository.create(new_product)
        if created_product is None:
            return CustomResponse.error('Product not created')
        return CustomResponse.ok(ProductSchema.from_orm(created_product).dict())

    async def update(self, product_id: int, product: ProductUpdateSchema):
        updated_product = await self.repository.update(product_id, product)
        if updated_product is None:
            return CustomResponse.error('Product not updated')
        return CustomResponse.ok()

    async def soft_delete(self, product_id: int):
        product_schema = ProductSoftDeleteSchema(id=product_id, is_active=False)
        deleted_product = await self.repository.update(product_id, product_schema)
        if deleted_product is None:
            return CustomResponse.error('Product not deleted')
        return CustomResponse.ok()
