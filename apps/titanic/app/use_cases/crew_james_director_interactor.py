from __future__ import annotations

from titanic.adapter.inbound.api.schemas.crew_james_director_schema import JamesDirectorSchema, FileUploadSchema
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort
from titanic.app.dtos.crew_james_director_dto import BookingCommand, JamesDirectorQuery, JamesDirectorResponse, PersonCommand


class JamesDirectorInteractor(JamesDirectorUseCase):
    def __init__(self, repository: JamesDirectorPort) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: JamesDirectorSchema) -> JamesDirectorResponse:
        '''제임스 감독의 자기소개 인터렉트'''
        
        return  await self.repository.introduce_myself(JamesDirectorQuery(
            id = schema.id,
            name = schema.name
        ))


    async def upload_titanic_file(self, schema: list[FileUploadSchema]) -> dict:
        person_commands = [
            PersonCommand(
                passenger_id=record.passenger_id or "",
                name=record.name or "",
                gender=record.gender or "",
                age=record.age or "",
                sib_sp=record.sib_sp or "",
                parch=record.parch or "",
                survived=str(record.survived) if record.survived is not None else "",
            )
            for record in schema
        ]
        booking_commands = [
            BookingCommand(
                pclass=record.pclass or "",
                ticket=record.ticket or "",
                fare=str(record.fare) if record.fare is not None else "",
                cabin=record.cabin or "",
                embarked=record.embarked or "",
            )
            for record in schema
        ]

        saved = await self.repository.receive_uploaded_records(person_commands, booking_commands)
        return {"saved": saved}