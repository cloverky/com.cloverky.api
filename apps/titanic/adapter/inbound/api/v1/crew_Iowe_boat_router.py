from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.adapter.inbound.api.schemas.crew_Iowe_boat_schema import LoweBoatSchema
from clover.apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatResponse
from clover.apps.titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from clover.apps.titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from clover.apps.titanic.dependencies.crew_hartley_violin_provider import get_hartley_violin_use_case
from clover.apps.titanic.dependencies.crew_lowe_boat_provider import get_lowe_boat_use_case
'''
해롤드 로우 (Harold Lowe - 타이타닉 5등 항해사)
구명보트(14호)를 이끌고 유일하게 지원자를 구하러 되돌아옴
'''
lowe_boat_router = APIRouter(prefix="/titanic/lowe", tags=["lowe"])

@lowe_boat_router.get("/myself")
async def introduce_myself(
    lowe: LoweBoatUseCase = Depends(get_lowe_boat_use_case)
) -> LoweBoatResponse:
    return await lowe.introduce_myself(
        LoweBoatSchema(
            id=5,
            name="해롤드 로우 (Harold Lowe)"
        )
    )
