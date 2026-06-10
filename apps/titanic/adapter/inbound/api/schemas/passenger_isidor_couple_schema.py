from pydantic import BaseModel, Field

class PassengerIsidorCoupleSchema(BaseModel):

    id: int = Field(0, description="Passenger ID")
    name: str = Field("이시도르 스트라우스", description="Passenger's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 9,
                "name": "Isidor Straus",
            }
        }
    }

IsidorCoupleSchema = PassengerIsidorCoupleSchema