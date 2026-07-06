from fastapi import APIRouter, Depends

from clover.apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse
from clover.apps.titanic.app.ports.input.crew_hartley_violin_use_case import (
    HartleyViolinUseCase,
)
from clover.apps.titanic.dependencies.crew_hartley_violin_provider import (
    get_hartley_violin_use_case,
)
from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import (
    HartleyViolinSchema,
)

"""
왈리스 하틀리 (Wallace Hartley - 악단장)
배가 가라앉는 극도의 공포 속에서도 승객들을 진정시키기 위해 끝까지 찬송가 '내 주를 가까이 하게 함은(Nearer, My God, to Thee)'을 연주했던 악단장입니다. 영화에서 가장 눈물지게 만드는 명장면의 주인공입니다. 배경 작업(Background Worker)이나 알림/이벤트 스트리밍 라우터에 어울립니다.

추천 파일명: hartley_violin_router.py (Violin: 마지막까지 켜던 바이올린)
"""
hartley_violin_router = APIRouter(prefix="/hartley", tags=["hartley"])


@hartley_violin_router.get("/myself")
async def introduce_myself(
    hartley: HartleyViolinUseCase = Depends(get_hartley_violin_use_case),
) -> HartleyViolinResponse:
    return await hartley.introduce_myself(
        HartleyViolinSchema(id=3, name="왈리스 하틀리 (Wallace Hartley)")
    )
