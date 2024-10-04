from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name: str
    email: str
    password: str
    password2: str

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    password2: str | None = None

    class Config:
        from_attributes = True
        exclude_unset = True


class UserForCreateSchema(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    is_admin: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class UserLoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
