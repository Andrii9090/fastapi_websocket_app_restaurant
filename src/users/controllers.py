import logging
from functools import wraps

import jwt
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError

from core.config import JWT_SECRET, BCRYPT_SECRET
from core.http_response import CustomResponse
from core.interfaces.abstract_user_repository import AbstractUserRepository
from users.schemas import UserCreateSchema, UserLoginSchema, UserForCreateSchema, UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserController:
    def __init__(self, repository: AbstractUserRepository):
        self.repository = repository

    async def create(self, user: UserCreateSchema):
        try:
            if not user.password == user.password2:
                return CustomResponse.error('Passwords do not match')
            user_create = UserForCreateSchema(name=user.name, email=user.email, password=self._get_hash(user.password))
            user = await self.repository.create(user_create)
            return CustomResponse.ok(UserSchema.from_orm(user).dict())
        except SQLAlchemyError as e:
            logging.error(e)
            return CustomResponse.error('User already exists')

    async def update(self, user_id: int, user: UserCreateSchema):
        try:
            user_updated = await self.repository.update(user_id, user)
            if user_updated:
                return CustomResponse.ok()
            return CustomResponse.error('User not updated')
        except SQLAlchemyError as e:
            logging.warning(e)
            return CustomResponse.error('User not found')

    async def get_by_id(self, user_id: int):
        try:
            user = await self.repository.get_by_id(user_id)
            return CustomResponse.ok(UserSchema.from_orm(user).dict())
        except SQLAlchemyError as e:
            logging.warning(e)
            return CustomResponse.error('User not found')

    async def login(self, user_data: UserLoginSchema):
        user = await self.repository.get_by_email(user_data.email)
        if user and self._verify_password(user_data.password, user.password):
            return CustomResponse.ok({'token': self._generate_token(user.id)})
        else:
            return CustomResponse.error('Wrong email or password')

    async def set_inactive(self, user_id: int):
        try:
            await self.repository.set_inactive(user_id)
            return CustomResponse.ok()
        except SQLAlchemyError as e:
            logging.warning(e)
            return CustomResponse.error('User not found')
        except Exception as e:
            logging.warning(e)
            return CustomResponse.error('The error occurred')

    async def get_all(self, limit: int = 100, offset: int = 0, where: object = None):
        users = await self.repository.get_all(limit, offset, where)
        return CustomResponse.ok([UserSchema.from_orm(user).dict() for user in users])

    @staticmethod
    def _get_hash(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(password, password_hash):
        return pwd_context.verify(password, password_hash)

    @staticmethod
    def _generate_token(user_id):
        return jwt.encode({'user_id': user_id}, key=JWT_SECRET, algorithm='HS256')

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, key=JWT_SECRET, algorithms=['HS256'])
