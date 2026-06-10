from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from clover.apps.titanic.app.dtos.passenger_ruth_survivor_dto import RuthValidationQuery, RuthValidationResponse


class RuthValidationRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: RuthValidationQuery) -> RuthValidationResponse:
        '''앤드류 설계자의 자기 소개 레포지토리 추상 메소드'''
        pass
    