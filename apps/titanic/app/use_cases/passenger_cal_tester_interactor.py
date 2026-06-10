from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from clover.apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from clover.apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from clover.apps.titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository


class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(CalTesterQuery(
            id=schema.id,
            name=schema.name
        ))
