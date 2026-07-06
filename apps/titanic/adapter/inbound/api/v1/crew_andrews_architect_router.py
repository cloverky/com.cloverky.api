from fastapi import APIRouter, Depends

from clover.apps.titanic.app.dtos.crew_andrews_architect_dto import (
    AndrewsArchitectResponse,
)
from clover.apps.titanic.app.ports.input.crew_andrews_architect_use_case import (
    AndrewsArchitectUseCase,
)
from clover.apps.titanic.dependencies.crew_andrews_architect_provider import (
    get_andrews_architect_use_case,
)
from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import (
    AndrewsArchitectSchema,
)

"""
토마스 앤드류스 (Thomas Andrews)
타이타닉을 설계한 수석 디자이너입니다. 배의 침몰을 가장 먼저 직감하고, 마지막 순간 흡연실 시계 앞에서 죄책감에 잠겨 있던 모습이 관객들에게 깊은 여운을 남겼습니다. 시스템의 구조나 메타데이터를 다루는 역할로 좋습니다.

추천 파일명: andrews_architect_router.py (Architect: 타이타닉 설계자)
"""
andrews_architect_router = APIRouter(prefix="/andrews", tags=["andrews"])


@andrews_architect_router.get("/myself")
async def introduce_myself(
    andrews: AndrewsArchitectUseCase = Depends(get_andrews_architect_use_case),
) -> AndrewsArchitectResponse:
    return await andrews.introduce_myself(
        AndrewsArchitectSchema(id=2, name="토마스 앤드류스 (Thomas Andrews)")
    )
