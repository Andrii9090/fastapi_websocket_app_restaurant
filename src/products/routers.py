from fastapi import APIRouter, Depends

from products.controllers import ProductController
from products.depends import get_product_controller
from products.schemas import ProductSchema, ProductCreateBodySchema, ProductUpdateSchema
from users.decorators import admin_required
from users.depends import get_auth_user

router = (
    APIRouter(
        prefix='/products',
        tags=['Products'],
        responses={404: {'description': 'Not found'}}
    ))


@router.post('/')
@admin_required
async def create_product(product: ProductCreateBodySchema,
                         controller: ProductController = Depends(get_product_controller),
                         auth_user=Depends(get_auth_user)):
    result = await controller.create(product, auth_user.id)
    return result


@router.get('/')
async def get_products(limit: int = 100, offset: int = 0,
                       controller: ProductController = Depends(get_product_controller)):
    result = await controller.get_all(limit, offset)
    return result


@router.get('/{product_id}')
async def get_product(product_id: int, controller: ProductController = Depends(get_product_controller)):
    result = await controller.get_product(product_id)
    return result


@router.put('/{id}')
@admin_required
async def update_product(product_id: int, product: ProductUpdateSchema,
                         controller: ProductController = Depends(get_product_controller),
                         auth_user=Depends(get_auth_user)):
    result = await controller.update(product_id, product)
    return result


@router.delete('/{product_id}')
@admin_required
async def soft_delete_product(product_id: int, controller: ProductController = Depends(get_product_controller),
                              auth_user=Depends(get_auth_user)):
    result = await controller.soft_delete(product_id)
    return result
