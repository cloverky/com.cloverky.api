from __future__ import annotations

from abc import ABC, abstractmethod

from pandas import DataFrame
import pandas as pd

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse


class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def get_train_set(self) -> pd.DataFrame:
        '''survived 컬럼이 있는 데이터를 DataFrame으로 반환'''
        pass

    @abstractmethod
    async def get_test_set(self):
        '''survived 컬럼이 없는 데이터를 DataFrame으로 반환'''
        pass

    @abstractmethod
    async def get_total_count(self) -> int:
        '''passengers 테이블 전체 행 수 반환'''
        pass

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        pass
