from fastapi import APIRouter, Depends

from silicon_valley.adapter.inbound.api.schemas.piper_bighetti_hr_schema import BighettiHrSchema
from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrResponse
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import BighettiHrUseCase
from silicon_valley.dependencies.piper_bighetti_hr_provider import get_bighetti_hr_use_case

bighetti_hr_router = APIRouter(prefix="/bighetti", tags=["bighetti"])


@bighetti_hr_router.get("/myself")
async def introduce_myself(
    use_case: BighettiHrUseCase = Depends(get_bighetti_hr_use_case),
) -> BighettiHrResponse:
    return await use_case.introduce_myself(
        BighettiHrSchema(id=5, name="빅 헤드 (Nelson Bighetti)")
    )
