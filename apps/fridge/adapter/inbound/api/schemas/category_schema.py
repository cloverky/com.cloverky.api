from datetime import datetime

from pydantic import BaseModel, Field


class CategorySchema(BaseModel):
    # 식재료를 분류하는 카테고리 스키마
    name: str = Field("채소", description="카테고리명")
    sort_order: int = Field(0, description="정렬순서")
    created_at: datetime | None = Field(None, description="생성일시")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "채소",
                "sort_order": 1,
                "created_at": "2025-06-15T09:00:00Z",
            }
        }
    }
