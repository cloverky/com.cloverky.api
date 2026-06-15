from datetime import date, datetime

from pydantic import BaseModel, Field


class InventoryExpirySchema(BaseModel):
    # 소비기한 임박 재료를 최우선 분류하는 핵심 스키마. 레시피 추천의 입력 기반
    user_id: int = Field(0, description="사용자 일련번호")
    food_id: int = Field(0, description="음식 품목 일련번호")
    quantity: int = Field(1, description="수량")
    unit: str = Field("개", description="단위 (예: g, 개, ml)")
    expiry_date: date | None = Field(None, description="소비기한")
    purchased_date: date | None = Field(None, description="구매일자")
    expiry_is_estimated: bool = Field(False, description="소비기한 추정 여부")
    storage: str = Field("냉장", description="보관방법 (냉장·냉동·실온)")
    created_at: datetime | None = Field(None, description="생성일시")
    updated_at: datetime | None = Field(None, description="수정일시")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "food_id": 3,
                "quantity": 5,
                "unit": "개",
                "expiry_date": "2025-06-20",
                "purchased_date": "2025-06-15",
                "expiry_is_estimated": False,
                "storage": "냉장",
                "created_at": "2025-06-15T09:00:00Z",
                "updated_at": "2025-06-15T09:00:00Z",
            }
        }
    }
