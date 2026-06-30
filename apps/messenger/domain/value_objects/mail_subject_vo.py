from __future__ import annotations

from dataclasses import dataclass

_MAX_LEN = 200


@dataclass(frozen=True)
class MailSubject:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("메일 제목은 비어 있을 수 없습니다.")
        if len(self.value) > _MAX_LEN:
            raise ValueError(f"메일 제목은 {_MAX_LEN}자를 초과할 수 없습니다.")

    @classmethod
    def from_raw(cls, value: str) -> MailSubject:
        return cls(value=value.strip())

    def __str__(self) -> str:
        return self.value
