from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import BookingOrm
from titanic.app.dtos.passenger_jack_trainer_dto import (
    JackTrainerQuery,
    JackTrainerResponse,
)
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort


class JackTrainerPgRepository(JackTrainerPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        """잭 트레이너의 자기 소개 레포지토리 구현 메소드"""

        logger.info(
            f"[JackTrainerPgRepository] introduce_myself 진입 | request_data={query}"
        )

        response: JackTrainerResponse = JackTrainerResponse(
            id=query.id * 10000, name=query.name + "가 레포지토리에 다녀옴"
        )
        return response

    async def get_training_data(self) -> list[dict[str, Any]]:
        """생존 예측 모델 학습에 사용할 피처 데이터 조회"""
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .outerjoin(BookingOrm, BookingOrm.passenger_id == PersonOrm.id)
                .order_by(PersonOrm.id)
            )
        ).all()
        return [
            {
                "pclass": booking.pclass if booking else None,
                "gender": person.gender,
                "age": person.age,
                "sibsp": person.sib_sp,
                "parch": person.parch,
                "fare": booking.fare if booking else None,
                "survived": person.survived,
            }
            for person, booking in rows
        ]
