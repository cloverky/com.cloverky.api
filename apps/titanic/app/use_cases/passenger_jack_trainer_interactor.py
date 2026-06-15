import logging

from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger(__name__)


class JackTrainerInteractor:
    
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        self.kiwi = Kiwi()

    async def analyze_message_intent(self, user_message: str) -> dict:
        tokens = self.kiwi.tokenize(user_message)
        keywords = [t.form for t in tokens if t.tag in ("NNG", "NNP", "VV", "VA")]
        intent = "unknown"
        if any(t.form in ("몇", "얼마", "수", "명") for t in tokens):
            intent = "count_query"
        elif any(t.form in ("누구", "이름") for t in tokens):
            intent = "name_query"
        elif any(t.form in ("생존", "살", "죽") for t in tokens):
            intent = "survival_query"
        logger.info(f"[JackTrainerInteractor] analyze_message_intent | keywords={keywords}, intent={intent}")
        return {"keywords": keywords, "intent": intent}

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(JackTrainerQuery(
            id = schema.id,
            name = schema.name
        ))