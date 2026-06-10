from pydantic import BaseModel, Field

class WalterRoasterSchema(BaseModel):

    id: int = Field(0, description="Crew ID")
    name: str = Field("월터 로스터", description="Crew's name")
    memo: str = Field("", description="메모")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Walter Lord / Crew",
            }
        }
    }