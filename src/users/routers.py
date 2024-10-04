from functools import wraps

from fastapi import APIRouter, Depends

from users.decorators import auth_required, admin_required
from users.depends import get_user_controller, get_auth_user
from users.schemas import UserCreateSchema, UserLoginSchema, UserUpdateSchema, UserSchema

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}}
)


@router.get('/')
@admin_required
async def get_users(controller=Depends(get_user_controller), auth_user=Depends(get_auth_user)):
    users = await controller.get_all()
    return users


@router.get('/{user_id}')
@auth_required
async def get_user(user_id: int, controller=Depends(get_user_controller), auth_user=Depends(get_auth_user)):
    user = await controller.get_by_id(user_id)
    return user


@router.post('/')
async def create_user(user: UserCreateSchema, controller=Depends(get_user_controller)):
    user = await controller.create(user)
    return user


@router.put('/{user_id}')
@auth_required
async def update_user(user_id: int, user_update: UserUpdateSchema,
                      controller=Depends(get_user_controller), auth_user=Depends(get_auth_user)):
    user_updated = await controller.update(user_id, user_update)
    return user_updated


@router.delete('/{user_id}')
@admin_required
async def delete_user(user_id: int, controller=Depends(get_user_controller), auth_user=Depends(get_auth_user)):
    return await controller.set_inactive(user_id)


@router.post('/login')
async def login(user: UserLoginSchema, controller=Depends(get_user_controller)):
    return await controller.login(user)
