from fastapi import FastAPI

from products.routers import router as router_products
from orders.routers import router as router_orders
from users.routers import router as router_users

app = FastAPI()
app.include_router(router_products)
app.include_router(router_orders)
app.include_router(router_users)
