from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.silicon_valley.app.dtos.piper_bighetti_hr_dto import (
    BighettiHrQuery,
    BighettiHrResponse,
)


class BighettiHrPort(ABC):
    @abstractmethod
    def introduce_myself(self, query: BighettiHrQuery) -> BighettiHrResponse:
        """빅 헤드의 자기 소개 레포지토리 추상 메소드"""
        pass
