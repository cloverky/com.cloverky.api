from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_rose_model_orm import BookingOrm
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PersonOrm
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.output.crew_walter_roaster_repository import WalterRoasterRepository
import logging

logger = logging.getLogger(__name__)


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



class WalterRoasterPgRepository(WalterRoasterRepository):
    '''PostgreSQL을 이용한 월터의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: WalterRoasterQuery) -> WalterRoasterResponse:
        
        '''앤드류 설계자의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[WalterRoasterPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: WalterRoasterResponse = WalterRoasterResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴",
            memo= query.memo
        )
        return response