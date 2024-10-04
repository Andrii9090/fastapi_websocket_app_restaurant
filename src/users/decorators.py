from functools import wraps

from core.http_response import CustomResponse


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'auth_user' in kwargs and kwargs['auth_user'].is_active:
            return await func(*args, **kwargs)
        else:
            return CustomResponse.unauthorized()

    return wrapper


def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if 'auth_user' in kwargs and kwargs['auth_user'].is_active and kwargs['auth_user'].is_admin:
            return await func(*args, **kwargs)
        else:
            return CustomResponse.unauthorized()

    return wrapper
