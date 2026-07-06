from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.passenger_isidor_couple_dto import (
    IsidorCoupleResponse,
)
from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import (
    IsidorCoupleSchema,
)


class IsidorCoupleUseCase(ABC):
    @abstractmethod
    def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        """이시도어 커플의 자기소개 메소드"""
        pass
