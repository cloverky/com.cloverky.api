from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from clover.apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse


class CalTesterUseCase(ABC):

    @abstractmethod


    async def test_model(self, test_set) -> CalTesterResponse:
        '''칼 테스터가 제안한 모델들을 테스트 시키는 메소드'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 메소드'''
        pass