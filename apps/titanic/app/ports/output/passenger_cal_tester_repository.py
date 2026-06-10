from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse


class CalTesterRepository(ABC):
    
    @abstractmethod
    def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        '''칼 테스터의 자기 소개 레포지토리 추상 메소드'''
        pass
    