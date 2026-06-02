from __future__ import annotations

import logging
from typing import Any



from titanic.app.dtos.james_director_dto import BookingCommand, PersonCommand
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository

logger = logging.getLogger(__name__)


class JamesDirectorPgRepository(JamesDirectorRepository):
    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> dict[str, Any]:
        logger.info(
            "🍀 [JamesPg] 저장 시작 — person=%d, booking=%d",
            len(person_commands),
            len(booking_commands),
        )

        for index, command in enumerate(person_commands[:5], start=1):
            logger.info("🎀🎀🎀 [제임스 레포지터리] PersonCommand 상위 5개 레코드 %d/5 — %s", index, command)

        for index, command in enumerate(booking_commands[:5], start=1):
            logger.info("🎀🎀🎀🎀 [제임스 레포지터리] BookingCommand 상위 5개 레코드 %d/5 — %s", index, command)

        rows = [
            {
                "id": None,
                "passenger_id": int(command.passenger_id) if command.passenger_id else None,
                "name": command.name or None,
                "gender": command.gender or None,
            }
            for command in person_commands
        ]
        return {"count": len(person_commands), "rows": rows}
