from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.watcher_dto import WatcherTriageCommand, WatcherTriageResult


class WatcherUseCase(ABC):
    @abstractmethod
    async def triage(self, command: WatcherTriageCommand) -> WatcherTriageResult: ...
