from fastapi import APIRouter, Depends

from fridge.adapter.inbound.api.schemas.inventory_schema import InventoryExpirySchema
from clover.apps.fridge.app.dtos.inventory_dto import InventoryExpiryResponse
from clover.apps.fridge.app.ports.input.inventory_use_case import InventoryUseCase
from clover.apps.fridge.dependencies.inventory_provider import get_inventory_use_case

'''
인벤토리 소비기한 관리 (Inventory Expiry)
프로젝트의 핵심 기능. 소비기한이 가장 임박한 식재료를 최우선으로
분류하여 버려지는 음식물을 최소화한다. 레시피 추천의 핵심 입력 데이터를 담당한다.
'''

inventory_router = APIRouter(prefix="/inventory", tags=["inventory"])


@inventory_router.get("/urgent")
async def get_urgent_items(
    inventory: InventoryUseCase = Depends(get_inventory_use_case)
) -> InventoryExpiryResponse:
    return await inventory.get_urgent_items(
        InventoryExpirySchema(
            user_id=1,
            food_id=1,
            quantity=1,
            unit="개",
            storage="냉장",
        )
    )
