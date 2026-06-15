from fastapi import APIRouter, Depends

from fridge.adapter.inbound.api.schemas.foods_schema import FoodCatalogSchema
from clover.apps.fridge.app.dtos.foods_dto import FoodCatalogResponse
from clover.apps.fridge.app.ports.input.foods_use_case import FoodsUseCase
from clover.apps.fridge.dependencies.foods_provider import get_foods_use_case

'''
식재료 카탈로그 (Foods Catalog)
AI가 인식한 식재료를 등록하고 관리하는 카탈로그.
카테고리 분류와 기본 단위를 보유하며, 인벤토리에 등록되는
식품 마스터 데이터 역할을 담당한다.
'''

foods_router = APIRouter(prefix="/food", tags=["food"])


@foods_router.get("/catalog")
async def get_catalog(
    food: FoodsUseCase = Depends(get_foods_use_case)
) -> FoodCatalogResponse:
    return await food.get_catalog(
        FoodCatalogSchema(
            category_id=1,
            name="사과",
            default_unit="개",
        )
    )
