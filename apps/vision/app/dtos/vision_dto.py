from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionQuery:
    id: int
    name: str


@dataclass(frozen=True)
class VisionResponse:
    id: int
    name: str
    description: str
