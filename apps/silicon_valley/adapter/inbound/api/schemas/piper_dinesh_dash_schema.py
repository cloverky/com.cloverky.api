from pydantic import BaseModel, Field


class PiperDineshDashSchema(BaseModel):
    id: int = Field(0, description="Character ID")
    name: str = Field("디네쉬 추그타이", description="Character's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Dinesh Chugtai",
            }
        }
    }


DineshDashSchema = PiperDineshDashSchema
