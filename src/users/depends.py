import logging
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.http_response import CustomResponse
from core.interfaces.abstract_repository import AbstractRepository
from core.interfaces.abstract_user_repository import AbstractUserRepository
from database.connect import async_session_generator
from users.controllers import UserController
from users.models import User
from users.repositories import SQLUserRepository

from users.schemas import UserSchema

token_auth = HTTPBearer()


def get_user_repository(session=Depends(async_session_generator)) -> AbstractRepository:
    return SQLUserRepository(session, User)


def get_user_controller(user_repository: AbstractUserRepository = Depends(get_user_repository)) -> UserController:
    return UserController(user_repository)


async def get_auth_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(token_auth)],
                        repository=Depends(get_user_repository)):
    try:
        if credentials:
            token = credentials.credentials.encode('utf-8')
            user_id = UserController.decode_token(token)['user_id']
            user = await repository.get_by_id(user_id)
            return UserSchema.from_orm(user)
        else:
            return CustomResponse.error('Invalid token')
    except Exception as e:
        logging.warning(e)
