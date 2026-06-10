from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from clover.apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse


class RoseModelRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        '''앤드류 설계자의 자기 소개 레포지토리 추상 메소드'''
        pass
    