from typing import List, Union, Annotated

from fastapi import APIRouter, Depends, Header
from starlette.websockets import WebSocket, WebSocketDisconnect

from orders.depends import get_order_controller
from orders.models import OrderStatus
from orders.schemas import CreateOrderSchema, OrderCreateProduct
from orders.websockets.websocket_manager import WebSocketManager
from users.controllers import UserController
from users.decorators import auth_required, admin_required
from users.depends import get_auth_user

router = (
    APIRouter(
        prefix='/orders',
        tags=['Orders'],
        responses={404: {'description': 'Not found'}}
    ))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             authorization: Annotated[str, Header()] = None):
    user_id = UserController.decode_token(authorization.split(' ')[1])['user_id']
    await websocket.accept()
    websocket_manager = WebSocketManager()
    await websocket_manager.connect(user_id, websocket)

    while True:
        try:
            await websocket.receive()
        except WebSocketDisconnect:
            await websocket.close()
            await websocket_manager.disconnect(user_id)
        except RuntimeError:
            break


@router.post('/')
@auth_required
async def create_order(order: CreateOrderSchema, controller=Depends(get_order_controller),
                       auth_user=Depends(get_auth_user)):
    order = await controller.create(order, auth_user.id)
    websocket_manager = WebSocketManager()
    await websocket_manager.broadcast(order['data'])
    return order


@router.get('/{order_id}')
@auth_required
async def get_order(order_id: int, controller=Depends(get_order_controller), auth_user=Depends(get_auth_user)):
    order = await controller.get_by_id(order_id)
    return order


@router.get('/')
@auth_required
@admin_required
async def get_orders(limit: int = 100, offset: int = 0, controller=Depends(get_order_controller),
                     auth_user=Depends(get_auth_user)):
    orders = await controller.get_all(limit, offset)
    return orders


@router.patch('/{order_id}')
@auth_required
async def update_order_status(order_id: int, status: OrderStatus, controller=Depends(get_order_controller),
                              auth_user=Depends(get_auth_user)):
    order = await controller.update_order_status(order_id, status)
    return order


@router.post('/products/{order_id}')
async def add_product_to_order(order_id: int, order_products: List[OrderCreateProduct],
                               controller=Depends(get_order_controller)):
    order = await controller.add_order_product(order_id, order_products)
    return order
