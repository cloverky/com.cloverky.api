from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db
from titanic.adapter.inbound.api.schemas.passenger_rose_model_schemas import RoseModelSchema
from clover.apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse
from clover.apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from clover.apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case

'''
로즈 드윗 부카터 (Rose DeWitt Bukater)
상류층의 답답함에서 벗어나고자 하는 의지, 그리고
영화의 핵심 매개체인 '다이아몬드'와 관련된 키워드입니다.
'''

rose_model_router = APIRouter(prefix="/rose", tags=["rose"])


@rose_model_router.get("/myself")
async def introduce_myself(
    rose: RoseModelUseCase = Depends(get_rose_model_use_case)
) -> RoseModelResponse:
    return await rose.introduce_myself(
        RoseModelSchema(
            id=14,
            name="로즈 드윗 부카터 (Rose DeWitt Bukater)"
        )
    )

