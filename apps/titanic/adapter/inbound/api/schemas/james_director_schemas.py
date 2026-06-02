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


class TitanicRecordSchema(BaseModel):
    """Titanic CSV 1행 — CSV 헤더 Sex는 gender 필드로 매핑한다."""

    passenger_id: int = Field(validation_alias="PassengerId")
    survived: int = Field(validation_alias="Survived", ge=0, le=1)
    pclass: int = Field(validation_alias="Pclass", ge=1, le=3)
    name: str = Field(validation_alias="Name")
    gender: str = Field(validation_alias="Sex")
    age: float | None = Field(default=None, validation_alias="Age")
    sib_sp: int = Field(validation_alias="SibSp", ge=0, default=0)
    parch: int = Field(validation_alias="Parch", ge=0, default=0)
    ticket: str = Field(validation_alias="Ticket")
    fare: float = Field(validation_alias="Fare", ge=0)
    cabin: str | None = Field(default=None, validation_alias="Cabin")
    embarked: str | None = Field(default=None, validation_alias="Embarked")

    @field_validator("passenger_id", "survived", "pclass", "sib_sp", "parch", mode="before")
    @classmethod
    def coerce_int(cls, value: Any) -> int:
        return int(str(value).strip())

    @field_validator("fare", mode="before")
    @classmethod
    def coerce_fare(cls, value: Any) -> float:
        return float(str(value).strip())

    @field_validator("age", mode="before")
    @classmethod
    def coerce_age(cls, value: Any) -> float | None:
        if value is None:
            return None
        cleaned = str(value).strip()
        if not cleaned:
            return None
        return float(cleaned)

    @field_validator("cabin", "embarked", mode="before")
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
