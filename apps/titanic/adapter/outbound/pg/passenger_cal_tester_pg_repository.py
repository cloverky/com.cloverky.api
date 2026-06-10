from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse


class CalTesterPgRepository:
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        
        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[CalTesterPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: CalTesterResponse = CalTesterResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response