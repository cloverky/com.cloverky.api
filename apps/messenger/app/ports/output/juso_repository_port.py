from __future__ import annotations

from abc import ABC, abstractmethod

from messenger.app.dtos.juso_dto import (
    ContactUploadCommand,
    ContactUploadResult,
    JusoMessengerQuery,
    JusoMessengerResponse,
    JusoSearchCommand,
    JusoSearchResult,
)


class JusoRepositoryPort(ABC):
    @abstractmethod
    async def search(self, cmd: JusoSearchCommand) -> JusoSearchResult:
        """행정안전부 주소 API 또는 로컬 DB에서 주소를 조회한다"""

    @abstractmethod
    async def upload_contacts(self, cmd: ContactUploadCommand) -> ContactUploadResult:
        """연락처를 저장소에 저장한다"""

    @abstractmethod
    async def introduce_myself(
        self, query: JusoMessengerQuery
    ) -> JusoMessengerResponse:
        """주소 검색 서비스 자기소개 레포지토리 추상 메서드"""
