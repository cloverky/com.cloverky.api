from __future__ import annotations

import re
from dataclasses import dataclass

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        if not _EMAIL_RE.match(self.value):
            raise ValueError(f"유효하지 않은 이메일 주소: {self.value!r}")

    @classmethod
    def from_raw(cls, value: str) -> EmailAddress:
        return cls(value=value.strip().lower())

    def __str__(self) -> str:
        return self.value
