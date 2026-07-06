from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WalterRoasterQuery:
    id: int
    name: str
    memo: str


@dataclass
class WalterRoasterResponse:
    id: int
    name: str
    memo: str
