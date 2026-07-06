import importlib
import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

silicon_valley_router = APIRouter(prefix="/api/v1", tags=["silicon_valley"])

_routers = [
    (
        "silicon_valley.adapter.inbound.api.v1.piper_hendricks_ceo_router",
        "hendricks_ceo_router",
    ),
    (
        "silicon_valley.adapter.inbound.api.v1.piper_gilfoyle_sys_router",
        "gilfoyle_sys_router",
    ),
    (
        "silicon_valley.adapter.inbound.api.v1.piper_dinesh_dash_router",
        "dinesh_dash_router",
    ),
    ("silicon_valley.adapter.inbound.api.v1.piper_dunn_coo_router", "dunn_coo_router"),
    (
        "silicon_valley.adapter.inbound.api.v1.piper_bighetti_hr_router",
        "bighetti_hr_router",
    ),
]

for _mod, _attr in _routers:
    try:
        _m = importlib.import_module(_mod)
        silicon_valley_router.include_router(getattr(_m, _attr))
    except Exception as _e:
        logger.warning("silicon_valley 라우터 로드 실패 — %s: %s", _mod, _e)

__all__ = ["silicon_valley_router"]
