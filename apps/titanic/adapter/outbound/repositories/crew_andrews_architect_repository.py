from __future__ import annotations

import logging
from typing import Any

from kiwipiepy import Kiwi
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.constants.intent_map import INTENT_MAP
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.output.crew_andrews_architect_port import AndrewsArchitectPort

logger = logging.getLogger(__name__)


class AndrewsArchitectPgRepository(AndrewsArchitectPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: AndrewsArchitectQuery) -> AndrewsArchitectResponse:
        
        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[AndrewsArchitectRepository] introduce_myself 진입 | request_data={query}")
        
        response: AndrewsArchitectResponse = AndrewsArchitectResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response