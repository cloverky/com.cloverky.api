from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoQuery, HendricksCeoResponse


class HendricksCeoPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: HendricksCeoQuery) -> HendricksCeoResponse:
        '''리처드 헨드릭스의 자기 소개 레포지토리 추상 메소드'''
        pass
