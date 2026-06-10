from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from clover.apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse


class HartleyViolinUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''하틀리 바이올린의 자기소개 메소드'''
        pass