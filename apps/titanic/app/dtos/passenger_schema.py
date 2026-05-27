from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TitanicPassengerSchema(BaseModel):
    PassengerId: int = Field(..., description="승객 고유 ID")
    Survived: int = Field(..., ge=0, le=1, description="생존 여부 (0 = 사망, 1 = 생존)")
    Pclass: int = Field(..., ge=1, le=3, description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    Name: str = Field(..., description="이름")
    Sex: str = Field(..., description="성별 (male / female)")
    Age: Optional[float] = Field(default=None, description="나이")
    SibSp: int = Field(..., ge=0, description="함께 탑승한 자녀/배우자 수")
    Parch: int = Field(..., ge=0, description="함께 탑승한 부모/자녀 수")
    Ticket: str = Field(..., description="티켓 번호")
    Fare: float = Field(..., ge=0.0, description="탑승 요금")
    Cabin: Optional[str] = Field(default=None, description="수하물 번호")
    Boat: Optional[str] = Field(default=None, description="탈출한 구명보트 번호")
    Embarked: Optional[str] = Field(default=None, description="선착장 (C, Q, S)")

    @field_validator("Sex")
    @classmethod
    def validate_sex(cls, v: str) -> str:
        cleaned = v.strip().lower()
        if cleaned not in ("male", "female"):
            raise ValueError("Sex must be 'male' or 'female'")
        return cleaned

    @field_validator("Embarked")
    @classmethod
    def validate_embarked(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = v.strip().upper()
        if cleaned not in ("C", "Q", "S", ""):
            raise ValueError("Embarked must be 'C', 'Q', or 'S'")
        return cleaned or None
