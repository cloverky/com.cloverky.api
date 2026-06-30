from __future__ import annotations

import logging

from messenger.app.dtos.juso_dto import (
    ContactUploadCommand,
    ContactUploadResult,
    JusoMessengerQuery,
    JusoMessengerResponse,
    JusoSearchCommand,
    JusoSearchResult,
)
from messenger.app.ports.input.juso_use_case import JusoUseCase
from messenger.app.ports.output.juso_repository_port import JusoRepositoryPort

logger = logging.getLogger(__name__)


class JusoInteractor(JusoUseCase):
    def __init__(self, repository: JusoRepositoryPort) -> None:
        self._repository = repository

    async def search(self, cmd: JusoSearchCommand) -> JusoSearchResult:
        logger.info(
            "[JusoInteractor] 주소 검색 | keyword=%r page=%d", cmd.keyword, cmd.page
        )
        return await self._repository.search(cmd)

    async def upload_contacts(self, cmd: ContactUploadCommand) -> ContactUploadResult:
        logger.info("[JusoInteractor] 연락처 업로드 | 총 %d건", len(cmd.records))
        return await self._repository.upload_contacts(cmd)

    async def introduce_myself(
        self, query: JusoMessengerQuery
    ) -> JusoMessengerResponse:
        return await self._repository.introduce_myself(query)
