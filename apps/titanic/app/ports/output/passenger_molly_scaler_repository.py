from __future__ import annotations

from abc import ABC, abstractmethod

from clover.apps.titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse


class MollyScalerRepository(ABC):
    
    @abstractmethod
    def introduce_myself(self, query: MollyScalerQuery) -> MollyScalerResponse:
        '''몰리 스케일러의 자기 소개 레포지토리 추상 메소드'''
        pass
    