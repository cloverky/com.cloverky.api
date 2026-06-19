from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import BookingOrm
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort


class CalTesterPgRepository(CalTesterPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:

        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[CalTesterPgRepository] introduce_myself 진입 | request_data={query}")

        response: CalTesterResponse = CalTesterResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def get_passenger_data(self) -> list[dict[str, Any]]:
        """모델 테스트에 사용할 전체 승객 피처 데이터 조회"""
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .outerjoin(BookingOrm, BookingOrm.passenger_id == PersonOrm.id)
                .order_by(PersonOrm.id)
            )
        ).all()
        return [
            {
                "pclass":   booking.pclass if booking else None,
                "gender":   person.gender,
                "age":      person.age,
                "sibsp":    person.sib_sp,
                "parch":    person.parch,
                "fare":     booking.fare if booking else None,
                "survived": person.survived,
            }
            for person, booking in rows
        ]
