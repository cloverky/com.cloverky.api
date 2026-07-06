from abc import ABC, abstractmethod

from titanic.app.dtos.crew_walter_roaster_dto import (
    WalterRoasterQuery,
    WalterRoasterResponse,
)


class WalterRoasterPort(ABC):
    """월터의 승객 명단 관리 저장소"""

    @abstractmethod
    async def get_train_set(self):
        """survived 컬럼이 있는 데이터 전체를 DataFrame으로 반환"""
        pass

    @abstractmethod
    async def get_test_set(self):
        """survived 컬럼이 없는 데이터 전체를 DataFrame으로 반환"""
        pass

    @abstractmethod
    async def get_total_count(self) -> int:
        """passengers 테이블 전체 행 수 반환"""
        pass

    @abstractmethod
    def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        """월터의 자기 소개 레포지토리 추상 메소드"""
        pass
