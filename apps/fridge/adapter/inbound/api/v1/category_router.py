from fastapi import APIRouter, Depends

from clover.apps.fridge.app.dtos.category_dto import CategoryResponse
from clover.apps.fridge.app.ports.input.category_use_case import CategoryUseCase
from clover.apps.fridge.dependencies.category_provider import get_category_use_case
from fridge.adapter.inbound.api.schemas.category_schema import CategorySchema

"""
카테고리 (Category)
식재료를 채소·과일·육류·유제품 등으로 분류하는 마스터 데이터.
sort_order로 정렬 우선순위를 관리하며, 식재료 카탈로그(Food)와
인벤토리 조회 필터링의 기준 역할을 담당한다.
"""

category_router = APIRouter(prefix="/category", tags=["category"])


@category_router.get("/list")
async def get_list(
    category: CategoryUseCase = Depends(get_category_use_case),
) -> CategoryResponse:
    return await category.get_list(
        CategorySchema(
            name="채소",
            sort_order=1,
        )
    )
