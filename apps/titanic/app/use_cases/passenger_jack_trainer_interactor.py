import logging

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger(__name__)


class JackTrainerInteractor:
    
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(JackTrainerQuery(
            id = schema.id,
            name = schema.name
        ))