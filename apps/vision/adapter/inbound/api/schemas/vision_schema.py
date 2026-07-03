from __future__ import annotations

from pydantic import BaseModel


class VisionSchema(BaseModel):
    id: int
    name: str
