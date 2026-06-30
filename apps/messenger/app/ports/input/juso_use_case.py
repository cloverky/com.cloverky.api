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


class JusoUseCase(ABC):
    @abstractmethod
    async def search(self, cmd: JusoSearchCommand) -> JusoSearchResult:
        """키워드로 주소를 검색한다"""

    @abstractmethod
    async def upload_contacts(self, cmd: ContactUploadCommand) -> ContactUploadResult:
        """Google Contacts CSV 파싱 결과를 저장한다"""

    @abstractmethod
    async def introduce_myself(
        self, query: JusoMessengerQuery
    ) -> JusoMessengerResponse:
        """주소 검색 서비스 자기소개"""
