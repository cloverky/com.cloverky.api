from pydantic import BaseModel, Field


class PiperGilfoyleSysSchema(BaseModel):
    id: int = Field(0, description="Character ID")
    name: str = Field("버트람 길포일", description="Character's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Bertram Gilfoyle",
            }
        }
    }


GilfoyleSysSchema = PiperGilfoyleSysSchema
