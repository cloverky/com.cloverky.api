from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import (
    CalTesterSchema,
)
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case

"""
칼 캘던 하클리 (Caledon Hockley)
오만하고 부유한 자산가이자, 소유욕이 강하고 빌런으로서의
면모를 드러내는 키워드입니다.
승객 입력값 유효성 검사를 담당합니다.
"""

cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])


@cal_tester_router.get("/myself")
async def introduce_myself(
    cal: CalTesterUseCase = Depends(get_cal_tester_use_case),
) -> CalTesterResponse:
    return await cal.introduce_myself(
        CalTesterSchema(id=2, name="칼 캘던 하클리 (Caledon Hockley)")
    )
