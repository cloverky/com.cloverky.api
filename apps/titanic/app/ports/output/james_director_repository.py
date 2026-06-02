from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand


class JamesDirectorRepository(ABC):
    @abstractmethod
    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand], 
        booking_commands: list[BookingCommand],
    ) -> dict[str, Any]:
        pass
