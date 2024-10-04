from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    image: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


class ProductSoftDeleteSchema(BaseModel):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class ProductCreateBodySchema(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    image: str | None = None

    class Config:
        from_attributes = True


class ProductCreateSchema(ProductCreateBodySchema):
    user_id: int


class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(gt=0, default=None)
    image: str | None = None

    class Config:
        from_attributes = True
