from __future__ import annotations

from typing import Any

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_rose_model_strategies_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort
import logging

logger = logging.getLogger(__name__)


def _row_to_dict(person: PersonOrm, booking: BookingOrm | None) -> dict[str, Any]:
    return {
        "PassengerId": person.passenger_id,
        "Survived": person.survived,
        "Pclass": booking.pclass if booking else None,
        "Name": person.name,
        "gender": person.gender,
        "Age": person.age,
        "SibSp": person.sib_sp,
        "Parch": person.parch,
        "Ticket": booking.ticket if booking else None,
        "Fare": booking.fare if booking else None,
        "Cabin": booking.cabin if booking else None,
        "Embarked": booking.embarked if booking else None,
    }



class WalterRoasterPgRepository(WalterRoasterPort):
    '''PostgreSQL을 이용한 월터의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_train_set(self) -> pd.DataFrame:
        '''survived 컬럼이 존재하는 행만 조회해 DataFrame으로 반환'''
        stmt = (
            select(PersonOrm, BookingOrm)
            .outerjoin(BookingOrm, PersonOrm.id == BookingOrm.passenger_id)
            .where(PersonOrm.survived.is_not(None))
        )
        result = await self.session.execute(stmt)
        rows = [_row_to_dict(p, b) for p, b in result.all()]
        return pd.DataFrame(rows)

    async def get_test_set(self) -> pd.DataFrame:
        '''survived 컬럼이 없는 행만 조회해 DataFrame으로 반환'''
        stmt = (
            select(PersonOrm, BookingOrm)
            .outerjoin(BookingOrm, PersonOrm.id == BookingOrm.passenger_id)
            .where(PersonOrm.survived.is_(None))
        )
        result = await self.session.execute(stmt)
        rows = [_row_to_dict(p, b) for p, b in result.all()]
        return pd.DataFrame(rows)

    async def get_total_count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(PersonOrm))
        return result.scalar_one()

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        
        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[WalterRoasterPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: WalterRoasterResponse = WalterRoasterResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴",
            memo= query.memo
        )
        return response
