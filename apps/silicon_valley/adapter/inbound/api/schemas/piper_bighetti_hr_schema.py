from pydantic import BaseModel, Field


class PiperBighettiHrSchema(BaseModel):

    id: int = Field(0, description="Character ID")
    name: str = Field("빅 헤드", description="Character's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Big Head (Nelson Bighetti)",
            }
        }
    }

BighettiHrSchema = PiperBighettiHrSchema
