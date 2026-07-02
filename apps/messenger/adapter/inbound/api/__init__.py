import importlib
import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

messenger_router = APIRouter(prefix="/messenger", tags=["messenger"])

_routers = [
    ("messenger.adapter.inbound.api.v1.mail_router", "mail_router"),
    ("messenger.adapter.inbound.api.v1.receive_router", "receive_router"),
    ("messenger.adapter.inbound.api.v1.juso_router", "juso_router"),
    ("messenger.adapter.inbound.api.v1.discord_router", "discord_router"),
    ("messenger.adapter.inbound.api.v1.telegram_router", "telegram_router"),
]

for _mod, _attr in _routers:
    try:
        _m = importlib.import_module(_mod)
        messenger_router.include_router(getattr(_m, _attr))
    except Exception as _e:
        logger.warning("messenger 라우터 로드 실패 — %s: %s", _mod, _e)

__all__ = ["messenger_router"]
