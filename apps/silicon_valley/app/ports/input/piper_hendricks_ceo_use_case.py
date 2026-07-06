from __future__ import annotations

from abc import ABC, abstractmethod

from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_schema import (
    HendricksCeoSchema,
)

from clover.apps.silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    HendricksCeoResponse,
)


class HendricksCeoUseCase(ABC):
    @abstractmethod
    def introduce_myself(self, schema: HendricksCeoSchema) -> HendricksCeoResponse:
        """리처드 헨드릭스의 자기소개 메소드"""
        pass
