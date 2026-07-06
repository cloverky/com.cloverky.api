from pydantic import BaseModel, Field


class ChatSchema(BaseModel):
    message: str = Field(..., description="사용자가 입력한 자연어 메시지")

    _config = {
        "json_schema_extra": {
            "example": {
                "message": "탑승객이몇 명이야?",
            }
        }
    }


class SmithCaptainSchema(BaseModel):
    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
