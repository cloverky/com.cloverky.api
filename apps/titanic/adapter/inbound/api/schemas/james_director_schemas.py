from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator

JAMES_DIRECTOR_CSV_COLUMNS: tuple[str, ...] = (
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
)


class JamesDirectorPassengerSchema(BaseModel):
    """Titanic CSV 1행 — CSV 헤더 Sex는 gender 필드로 매핑한다."""

    PassengerId: int
    Survived: int = Field(ge=0, le=1)
    Pclass: int = Field(ge=1, le=3)
    Name: str
    gender: str = Field(validation_alias="Sex")
    Age: float | None = None
    SibSp: int = Field(ge=0, default=0)
    Parch: int = Field(ge=0, default=0)
    Ticket: str
    Fare: float = Field(ge=0)
    Cabin: str | None = None
    Embarked: str | None = None

    @field_validator("PassengerId", "Survived", "Pclass", "SibSp", "Parch", mode="before")
    @classmethod
    def coerce_int(cls, value: Any) -> int:
        return int(str(value).strip())

    @field_validator("Fare", mode="before")
    @classmethod
    def coerce_fare(cls, value: Any) -> float:
        return float(str(value).strip())

    @field_validator("Age", mode="before")
    @classmethod
    def coerce_age(cls, value: Any) -> float | None:
        if value is None:
            return None
        cleaned = str(value).strip()
        if not cleaned:
            return None
        return float(cleaned)

    @field_validator("Cabin", "Embarked", mode="before")
    @classmethod
    def empty_str_to_none(cls, value: Any) -> str | None:
        if value is None:
            return None
        cleaned = str(value).strip()
        return cleaned or None

    @field_validator("gender", mode="before")
    @classmethod
    def normalize_gender(cls, value: Any) -> str:
        return str(value).strip()


class JamesDirectorSavedRowSchema(BaseModel):
    id: int | None = None
    passenger_id: int | None = None
    name: str | None = None
    gender: str | None = None


class JamesDirectorUploadResponseSchema(BaseModel):
    message: str
    count: int
    columns: list[str]
    rows: list[JamesDirectorSavedRowSchema]
