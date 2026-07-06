import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

fridge_router = APIRouter(prefix="/api/fridge", tags=["fridge"])

_routers = [
    ("fridge.adapter.inbound.api.v1.user_router", "user_router"),
    ("fridge.adapter.inbound.api.v1.inventory_router", "inventory_router"),
    ("fridge.adapter.inbound.api.v1.foods_router", "foods_router"),
    ("fridge.adapter.inbound.api.v1.receipt_router", "receipt_router"),
    ("fridge.adapter.inbound.api.v1.receipt_line_router", "receipt_line_router"),
    ("fridge.adapter.inbound.api.v1.category_router", "category_router"),
]

for _mod, _attr in _routers:
    try:
        import importlib

        _m = importlib.import_module(_mod)
        fridge_router.include_router(getattr(_m, _attr))
    except Exception as _e:
        logger.warning("fridge 라우터 로드 실패 — %s: %s", _mod, _e)

__all__ = ["fridge_router"]
