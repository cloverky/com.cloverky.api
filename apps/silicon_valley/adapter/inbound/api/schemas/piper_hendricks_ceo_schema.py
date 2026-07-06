from pydantic import BaseModel, Field


class PiperHendricksCeoSchema(BaseModel):
    id: int = Field(0, description="Character ID")
    name: str = Field("리처드 헨드릭스", description="Character's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Richard Hendricks",
            }
        }
    }


HendricksCeoSchema = PiperHendricksCeoSchema
