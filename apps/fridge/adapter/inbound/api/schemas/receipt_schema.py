from datetime import date, datetime

from pydantic import BaseModel, Field


class ReceiptUploadSchema(BaseModel):
    # AI OCR이 영수증을 인식하기 전 사용자가 제출하는 메타데이터 스키마
    user_id: int = Field(0, description="사용자ID")
    store_name: str = Field("", description="매장명")
    purchased_date: date | None = Field(None, description="구매일자")
    status: str = Field("pending", description="처리 상태")
    created_at: datetime | None = Field(None, description="생성일시")

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "store_name": "이마트",
                "purchased_date": "2025-06-15",
                "status": "pending",
                "created_at": "2025-06-15T09:00:00Z",
            }
        }
    }
