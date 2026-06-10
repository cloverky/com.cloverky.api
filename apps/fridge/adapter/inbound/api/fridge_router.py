from fastapi import APIRouter

from fridge.adapter.inbound.api.v1.category_router import category_router
from fridge.adapter.inbound.api.v1.food_router import food_router
from fridge.adapter.inbound.api.v1.inventory_router import inventory_router
from fridge.adapter.inbound.api.v1.receipt_router import receipt_router

fridge_router = APIRouter(tags=["fridge"])

fridge_router.include_router(category_router)
fridge_router.include_router(food_router)
fridge_router.include_router(inventory_router)
fridge_router.include_router(receipt_router)
