from fastapi import APIRouter, Depends
from silicon_valley.adapter.inbound.api.schemas.piper_dunn_coo_schema import (
    DunnCooSchema,
)
from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooResponse
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import DunnCooUseCase
from silicon_valley.dependencies.piper_dunn_coo_provider import get_dunn_coo_use_case

dunn_coo_router = APIRouter(prefix="/dunn", tags=["dunn"])


@dunn_coo_router.get("/myself")
async def introduce_myself(
    use_case: DunnCooUseCase = Depends(get_dunn_coo_use_case),
) -> DunnCooResponse:
    return await use_case.introduce_myself(
        DunnCooSchema(id=4, name="재러드 던 (Jared Dunn)")
    )
