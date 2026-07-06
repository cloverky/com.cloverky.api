from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from clover.apps.titanic.app.dtos.passenger_cal_tester_dto import (
    CalTesterQuery,
    CalTesterResponse,
)


class CalTesterPort(ABC):
    @abstractmethod
    def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        """칼 테스터의 자기 소개 레포지토리 추상 메소드"""
        pass

    @abstractmethod
    async def get_passenger_data(self) -> list[dict[str, Any]]:
        """모델 테스트에 사용할 전체 승객 피처 데이터 조회"""
        pass
