from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.app.dtos.crew_smith_captain_dto import (
    SmithCaptainQuery,
    SmithCaptainResponse,
    SmithChatResponse,
)
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

logger = logging.getLogger(__name__)


class SmithCaptainPgRepository(SmithCaptainPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        logger.info(
            "[SmithCaptainPgRepository] introduce_myself 진입 | request_data=%s", query
        )
        return SmithCaptainResponse(
            id=query.id * 10000, name=query.name + "가 레포지토리에 다녀옴"
        )

    async def chat(self, message: str) -> SmithChatResponse:
        logger.info("[SmithCaptainPgRepository] chat 진입 | message=%r", message)
        from core.matrix.keymaker_api import get_keymaker

        keymaker = get_keymaker()
        if not keymaker.is_gemini_ready():
            raise ValueError(
                "GEMINI_API_KEY가 설정되지 않았습니다. clover/.env 에 키를 넣어 주세요."
            )
        client = keymaker.get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=message
        )
        return SmithChatResponse(reply=(response.text or "").strip())

    async def get_stats(self) -> dict[str, Any]:
        total = (
            await self.session.execute(select(func.count()).select_from(PersonOrm))
        ).scalar_one()
        survived = (
            await self.session.execute(
                select(func.count()).where(PersonOrm.survived == "1")
            )
        ).scalar_one()
        return {"total": total, "survived": survived, "perished": total - survived}
