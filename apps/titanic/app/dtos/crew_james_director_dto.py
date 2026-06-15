from dataclasses import dataclass

@dataclass
class PersonCommand:
    """Person 엔티티 — 3NF Person 테이블 컬럼 그대로 (타입은 str)."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str

@dataclass
class BookingCommand:
    """Booking + Port 역정규화 — country 제외, 타입은 str."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass
class JamesDirectorUploadResponse:
    answer : str

@dataclass
class JamesDirectorQuery:
    id: int
    name: str

@dataclass
class JamesDirectorResponse:
    id: int
    name: str
