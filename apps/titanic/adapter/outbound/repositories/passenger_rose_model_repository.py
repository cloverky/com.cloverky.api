from __future__ import annotations

from typing import Any

import logging

logger = logging.getLogger(__name__)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.app.ports.output.passenger_rose_model_port import RoseModelPort


def _row_to_dict(person: PersonOrm, booking: BookingOrm | None) -> dict[str, Any]:
    return {
        "id": person.id,
        "passenger": person.passenger_id,
        "survived": person.survived,
        "pclass": booking.pclass if booking else None,
        "name": person.name,
        "gender": person.gender,
        "age": person.age,
        "sibsp": person.sib_sp,
        "parch": person.parch,
        "ticket": booking.ticket if booking else None,
        "fare": booking.fare if booking else None,
        "cabin": booking.cabin if booking else None,
        "embarked": booking.embarked if booking else None,
    }


class RoseModelPgRepository(RoseModelPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        
        '''로즈 모델의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[RoseModelPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: RoseModelResponse = RoseModelResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def get_all_records(self) -> list[dict[str, Any]]:
        """ML 학습에 사용할 전체 승객 데이터 조회"""
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .outerjoin(BookingOrm, BookingOrm.passenger_id == PersonOrm.id)
                .order_by(PersonOrm.id)
            )
        ).all()
        return [_row_to_dict(person, booking) for person, booking in rows]
