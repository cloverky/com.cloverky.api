from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from clover.apps.titanic.app.dtos.crew_james_director_dto import BookingCommand, JamesDirectorQuery, JamesDirectorResponse, PersonCommand


class JamesDirectorPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: JamesDirectorQuery) -> JamesDirectorResponse:
        '''제임스 감독의 자기 소개 레포지토리 추상 메소드'''
        pass

    @abstractmethod
    async def receive_uploaded_records(self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand]) -> int:
        pass
