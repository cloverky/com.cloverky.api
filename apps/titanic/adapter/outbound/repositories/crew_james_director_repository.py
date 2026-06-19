from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.app.dtos.crew_james_director_dto import BookingCommand, JamesDirectorQuery, JamesDirectorResponse, PersonCommand
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort


class JamesDirectorPgRepository(JamesDirectorPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JamesDirectorQuery) -> JamesDirectorResponse:
        
        '''제임스 감독의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[JamesDirectorPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: JamesDirectorResponse = JamesDirectorResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def receive_uploaded_records(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        return await self.upload_titanic_file(person_commands, booking_commands)

    async def upload_titanic_file(
        self,
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        # passenger_id 기준 중복 skip (ON CONFLICT DO NOTHING)
        person_values = [
            {
                "passenger_id": str(cmd.passenger_id),
                "name": cmd.name,
                "gender": cmd.gender,
                "age": cmd.age,
                "sib_sp": cmd.sib_sp,
                "parch": cmd.parch,
                "survived": cmd.survived,
            }
            for cmd in person_commands
        ]
        insert_stmt = (
            pg_insert(PersonOrm)
            .values(person_values)
            .on_conflict_do_nothing(index_elements=["passenger_id"])
            .returning(PersonOrm.id, PersonOrm.passenger_id)
        )
        result = await self.session.execute(insert_stmt)
        inserted_rows = result.fetchall()

        if not inserted_rows:
            await self.session.commit()
            return 0

        # 새로 삽입된 passenger_id → id 매핑
        id_by_passenger_id = {row[1]: row[0] for row in inserted_rows}

        booking_orms = [
            BookingOrm(
                passenger_id=id_by_passenger_id[str(person_cmd.passenger_id)],
                pclass=booking_cmd.pclass,
                ticket=booking_cmd.ticket,
                fare=booking_cmd.fare,
                cabin=booking_cmd.cabin,
                embarked=booking_cmd.embarked,
            )
            for person_cmd, booking_cmd in zip(person_commands, booking_commands)
            if str(person_cmd.passenger_id) in id_by_passenger_id
        ]
        self.session.add_all(booking_orms)
        await self.session.commit()

        return len(booking_orms)
