from pydantic import BaseModel
from sqlalchemy import select

from core.interfaces.abstract_repository import AbstractRepository


class SQLRepository(AbstractRepository):

    def __init__(self, session, model):
        self.session = session
        self.model = model
        super().__init__()

    async def create(self, new_item: BaseModel):
        new = self.model(**new_item.dict())
        self.session.add(new)
        await self.session.commit()
        await self.session.refresh(new)
        return new

    async def update(self, item_id: int, updated_item) -> bool:
        item = await self.get_by_id(item_id)
        if item is not None:
            for key, value in updated_item.dict(exclude_unset=True).items():
                setattr(item, key, value)
            self.session.add(item)
            await self.session.commit()
            return True
        return False

    async def delete(self, item_id: int) -> bool:
        item = await self.get_by_id(item_id)
        if item is not None:
            await self.session.delete(item)
            await self.session.commit()
            return True
        return False

    async def get_by_id(self, item_id: int):
        result = await self.session.execute(select(self.model).filter(self.model.id == item_id))
        return result.scalars().first()

    async def get_all(self, limit, offset, where=None, order_by=None):
        if order_by is None:
            order_by = self.model.id
        if where is None:
            result = await self.session.execute(
                select(self.model).limit(limit).offset(offset).order_by(order_by.desc()))
        else:
            result = await self.session.execute(
                select(self.model).where(where).limit(limit).offset(offset).order_by(order_by))
        return result.scalars().all()
