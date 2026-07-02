import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

"""
왓슨 (Watson Watcher Hub)
인바운드 메일 이벤트의 초진 분류 관문 (Triage Nurse).
발신자 중요도와 본문 의도를 분석해 Holmes 또는 Faker로 라우팅을 결정한다.
"""

watcher_router = APIRouter(prefix="/watcher", tags=["watcher"])


@watcher_router.get("/myself")
async def introduce_myself():
    return {"id": 1, 
            "name": "왓슨 (Watson Watcher Hub)", 
            "role": "Triage Nurse — Holmes / Faker 라우팅 결정"
            }


