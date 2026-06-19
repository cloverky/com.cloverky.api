from fastapi import APIRouter, Depends

from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_schema import HendricksCeoSchema
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import HendricksCeoResponse
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import HendricksCeoUseCase
from silicon_valley.dependencies.piper_hendricks_ceo_provider import get_hendricks_ceo_use_case

hendricks_ceo_router = APIRouter(prefix="/hendricks", tags=["hendricks"])


@hendricks_ceo_router.get("/myself")
async def introduce_myself(
    use_case: HendricksCeoUseCase = Depends(get_hendricks_ceo_use_case),
) -> HendricksCeoResponse:
    return await use_case.introduce_myself(
        HendricksCeoSchema(id=1, name="리처드 헨드릭스 (Richard Hendricks)")
    )
