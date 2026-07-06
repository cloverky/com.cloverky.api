from dataclasses import dataclass


@dataclass(frozen=True)  # 생성 후 수정 불가하도록 설정
class IoweBoatQuery:
    id: int
    name: str


LoweBoatQuery = IoweBoatQuery


@dataclass(frozen=True)
class IoweBoatResponse:
    id: int
    name: str


LoweBoatResponse = IoweBoatResponse
