from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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