from datetime import datetime

from pydantic import BaseModel, Field


class FoodCatalogSchema(BaseModel):
    # AI가 인식한 식재료를 카탈로그에 등록하는 스키마
    category_id: int = Field(0, description="카테고리 ID (사용자ID)")
    name: str = Field("사과", description="품목명")
    description: str = Field("", description="상세설명")
    default_unit: str = Field("개", description="기본 단위 (예: g, 개, ml)")
    created_at: datetime | None = Field(None, description="생성일시")
    updated_at: datetime | None = Field(None, description="수정일시")

    model_config = {
        "json_schema_extra": {
            "example": {
                "category_id": 1,
                "name": "사과",
                "description": "국내산 부사 사과",
                "default_unit": "개",
                "created_at": "2025-06-15T09:00:00Z",
                "updated_at": "2025-06-15T09:00:00Z",
            }
        }
    }
