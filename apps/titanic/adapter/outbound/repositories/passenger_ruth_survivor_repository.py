from __future__ import annotations

from typing import Any

import logging

logger = logging.getLogger(__name__)
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.passenger_ruth_survivor_dto import RuthValidationQuery, RuthValidationResponse
from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.app.ports.output.passenger_ruth_survivor_port import RuthValidationPort


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


class RuthValidationPgRepository(RuthValidationPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RuthValidationQuery) -> RuthValidationResponse:
        
        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[RuthValidationPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: RuthValidationResponse = RuthValidationResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def list_by_pclass(
        self, pclass: int, page: int, page_size: int
    ) -> tuple[int, list[dict[str, Any]]]:
        """등급(pclass)으로 필터링한 승객 목록 페이지네이션 조회"""
        pclass_str = str(pclass)
        total = (
            await self.session.execute(
                select(func.count())
                .select_from(PersonOrm)
                .join(BookingOrm, BookingOrm.passenger_id == PersonOrm.id)
                .where(BookingOrm.pclass == pclass_str)
            )
        ).scalar_one()
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .join(BookingOrm, BookingOrm.passenger_id == PersonOrm.id)
                .where(BookingOrm.pclass == pclass_str)
                .order_by(PersonOrm.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
        ).all()
        items = [_row_to_dict(person, booking) for person, booking in rows]
        return total, items
