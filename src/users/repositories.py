from sqlalchemy import select

from core.interfaces.SQLRepository import SQLRepository
from core.interfaces.abstract_user_repository import AbstractUserRepository


class SQLUserRepository(SQLRepository, AbstractUserRepository):

    def __init__(self, session, model):
        super().__init__(session, model)

    async def get_by_email(self, email):
        user = await self.session.execute(select(self.model).filter(self.model.email == email))
        return user.scalar()

    async def set_inactive(self, user_id: int):
        user = await self.get_by_id(user_id)

        user.is_active = False
        await self.session.commit()
