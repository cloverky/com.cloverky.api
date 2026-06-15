from pydantic import BaseModel, Field


class ReceiptLineSchema(BaseModel):
    # AI OCR이 영수증에서 인식한 품목 한 줄의 스키마. raw_text로 원문 보존
    receipt_id: int = Field(0, description="영수증 ID")
    line_name: str = Field("", description="품목 표기명")
    quantity: int = Field(1, description="수량")
    unit: str = Field("개", description="단위")
    raw_text: str = Field("", description="인식된 원문 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "receipt_id": 1,
                "line_name": "사과",
                "quantity": 3,
                "unit": "개",
                "raw_text": "사과 3개 2,990원",
            }
        }
    }
