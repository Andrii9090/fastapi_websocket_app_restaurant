from sqlalchemy import select

from core.interfaces.SQLRepository import SQLRepository
from products.models import Product


class ProductRepository(SQLRepository):
    def __init__(self, session):
        super().__init__(session, Product)

    async def get_all(self, limit, offset, where=None, order_by=None):
        if order_by is None:
            order_by = Product.id
        if where is None:
            result = await self.session.execute(
                select(Product).where(Product.is_active.is_(True)).limit(limit).offset(offset).order_by(
                    order_by.desc()))
        else:
            result = await self.session.execute(
                select(Product).where(where).limit(limit).offset(offset).order_by(order_by))
        return result.scalars().all()
