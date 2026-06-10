import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])

_routers = [
    ("titanic.adapter.inbound.api.v1.crew_james_director_router", "james_director_router"),
    ("titanic.adapter.inbound.api.v1.crew_walter_roaster_router", "walter_roaster_router"),
    ("titanic.adapter.inbound.api.v1.crew_andrews_architect_router", "andrews_architect_router"),
    ("titanic.adapter.inbound.api.v1.crew_hartley_violin_router", "hartley_violin_router"),
    ("titanic.adapter.inbound.api.v1.crew_Iowe_boat_router", "lowe_boat_router"),
    ("titanic.adapter.inbound.api.v1.crew_smith_captain_router", "smith_captain_router"),
    ("titanic.adapter.inbound.api.v1.passenger_cal_tester_router", "cal_tester_router"),
    ("titanic.adapter.inbound.api.v1.passenger_isidor_couple_router", "isidor_couple_router"),
    ("titanic.adapter.inbound.api.v1.passenger_jack_trainer_router", "jack_trainer_router"),
    ("titanic.adapter.inbound.api.v1.passenger_molly_scaler_router", "molly_scaler_router"),
    ("titanic.adapter.inbound.api.v1.passenger_rose_model_router", "rose_model_router"),
    ("titanic.adapter.inbound.api.v1.passenger_ruth_survivor_router", "ruth_validation_router"),
]

for _mod, _attr in _routers:
    try:
        import importlib
        _m = importlib.import_module(_mod)
        titanic_router.include_router(getattr(_m, _attr))
    except Exception as _e:
        logger.warning("titanic 라우터 로드 실패 — %s: %s", _mod, _e)

__all__ = ["titanic_router"]
