from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DeckZone(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    UNKNOWN = "U"


@dataclass(frozen=True)
class Cabin:
    value: str
    deck: DeckZone

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Cabin":
        if raw is None or raw.strip() == "":
            return cls(value="Unknown", deck=DeckZone.UNKNOWN)
        stripped = raw.strip()
        first = stripped[0].upper()
        valid = {d.value for d in DeckZone if d != DeckZone.UNKNOWN}
        deck = DeckZone(first) if first in valid else DeckZone.UNKNOWN
        return cls(value=stripped, deck=deck)

    @property
    def is_upper_deck(self) -> bool:
        return self.deck in {DeckZone.A, DeckZone.B, DeckZone.C}

    def __str__(self) -> str:
        return self.value
