from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from clover.apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse

class JackTrainerRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        '''잭 트레이너의 자기 소개 레포지토리 추상 메소드'''
        pass
    