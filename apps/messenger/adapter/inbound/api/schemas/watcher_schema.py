from __future__ import annotations

from pydantic import BaseModel

from messenger.app.dtos.watcher_dto import RoutingDecision


class WatcherRequest(BaseModel):
    from_email: str
    subject: str | None = None
    body: str | None = None
    important_client: bool = False


class WatcherResponse(BaseModel):
    routing: RoutingDecision
    reason: str
