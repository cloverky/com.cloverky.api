from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RoutingDecision(str, Enum):
    HOLMES = "holmes"
    FAKER = "faker"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class WatcherTriageCommand:
    from_email: str
    subject: str | None
    body: str | None
    mail_id: int | None = None
    important_client: bool = False


@dataclass(frozen=True)
class WatcherTriageResult:
    routing: RoutingDecision
    reason: str
