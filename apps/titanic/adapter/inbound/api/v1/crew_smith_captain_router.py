import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from titanic.dependencies.crew_smith_captain_provider import SmithCaptainUseCase
from titanic.dependencies.passenger_rose_model_provider import RoseModelUseCase
from titanic.dependencies.passenger_jack_trainer_provider import JackTrainerUseCase
from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatSchema, SmithCaptainSchema
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case
from titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case

logger = logging.getLogger(__name__)

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.

추천 파일명: smith_captain_router.py (또는 smith_wheel_router.py)
'''

smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat")
async def chat(
    schema: Annotated[ChatSchema, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
    jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
    rose: RoseModelUseCase = Depends(get_rose_model_use_case)
):
    logger.info("스미스 채팅 수신 — message: %r", schema.message)
    try:
        return await smith.chat(schema, jack, rose)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    



@smith_captain_router.get("/myself")
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case)
):
    return await smith.introduce_myself(
        SmithCaptainSchema(
            id=6,
            name="스미스 선장 (Captain Edward John Smith)"
        )
    )