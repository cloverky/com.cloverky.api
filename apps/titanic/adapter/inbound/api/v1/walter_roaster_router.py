from fastapi import APIRouter
from apps.titanic.adapter.inbound.api.schemas.walter_roaster_schemas import WalterRoasterSchema
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.use_cases.walter_roaster_interactor import WalterRoasterInteractor
import logging

logger = logging.getLogger(__name__)
walter_router = APIRouter(prefix="/titanic/walter", tags=["walter"])

@walter_roaster_router.get("/myself")
async def introduce_myself():
    schema = WalterRoasterSchema()

    logger.info("##################################################")
    logger.info("🎁 [월터 라우터] 월터의 자기소개글을 가져오는 API 호출")
    logger.info(f"🎁 ID: {schema.id}")
    logger.info(f"🎁 이름: {schema.name}")
    logger.info(f"🎁 비고: {schema.memo}")
    logger.info("##################################################")

    walter : WalterRoasterUseCase = WalterRoasterInteractor()
    walter.introduce_myself(schema)
    pass