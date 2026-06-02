from __future__ import annotations

import logging
from typing import Any

from titanic.adapter.outbound.pg.james_director_pg_repository import JamesDirectorPgRepository
from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository

logger = logging.getLogger(__name__)


class JamesDirectorInteractor(JamesDirectorUseCase):
    """JamesUseCase 구현 — JamesRepository(저장 포트)만 의존한다."""

    def __init__(self, repository: JamesDirectorRepository | None = None) -> None:
        self._repository = repository or JamesDirectorPgRepository()


    async def receive_uploaded_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        person_commands: list[PersonCommand] = []
        booking_commands: list[BookingCommand] = []

        for record in records:
            # schema 를 PersonCommand 및 BookingCommand 로 나눠서 옮겨담기
            person_commands.append(
                PersonCommand(
                    passenger_id=str(record.get("passenger_id", "")),
                    name=str(record.get("name", "")),
                    gender=str(record.get("gender") or ""),
                    age=str(record.get("Age", "")),
                    sib_sp=str(record.get("sib_sp", "")),
                    parch=str(record.get("parch", "")),
                    survived=str(record.get("survived", "")),
                ),
            )
            booking_commands.append(
                BookingCommand(
                    pclass=str(record.get("pclass", "")),
                    ticket=str(record.get("ticket", "")),
                    fare=str(record.get("fare", "")),
                    cabin=str(record.get("cabin") or ""),
                    embarked=str(record.get("embarked") or ""),
                ),
            )

        for index, record in enumerate(records[:5], start=1):
            print(
                f"🎀🎀 [제임스 유스케이스] 라우터에서 유스케이스로 옮겨진 스키마 상위 5개 레코드 {index}/5 — {record}",
            )
        return await self._repository.receive_uploaded_records(person_commands, booking_commands)
