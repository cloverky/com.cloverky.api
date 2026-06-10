from __future__ import annotations

from typing import Any

import logging

logger = logging.getLogger(__name__)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm


class SmithCaptainPgRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        
        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[SmithCaptainPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: SmithCaptainResponse = SmithCaptainResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def get_stats(self) -> dict[str, Any]:
        """전체 승객 생존/사망 통계 조회"""
        total = (
            await self.session.execute(select(func.count()).select_from(PersonOrm))
        ).scalar_one()
        survived = (
            await self.session.execute(
                select(func.count()).where(PersonOrm.survived == "1")
            )
        ).scalar_one()
        return {"total": total, "survived": survived, "perished": total - survived}