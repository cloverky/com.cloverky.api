from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.passenger_isidor_couple_dto import (
    IsidorCoupleQuery,
    IsidorCoupleResponse,
)


class IsidorCouplePort(ABC):
    @abstractmethod
    def introduce_myself(self, query: IsidorCoupleQuery) -> IsidorCoupleResponse:
        """이시도어 커플의 자기 소개 레포지토리 추상 메소드"""
        pass
