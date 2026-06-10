import logging

from fastapi import APIRouter, Depends
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster import get_walter_roaster_use_case

'''
영화 <타이타닉>에서 승객 명단을 관리하는 
일등 항해사 윌터 와일딩(Walter Nichols / 혹은 윌리엄 머독 등 영화 속 관리자 캐릭터) 
또는 승객 명단(Passenger List)을 다루는 '월터'라는 인물의 상황에 맞추어, 
직관적이면서도 센스 있는 중간 키워드를 추천해 드립니다.
'''
logger = logging.getLogger(__name__)
walter_roaster_router = APIRouter(prefix="/titanic/walter", tags=["walter"])    

@walter_roaster_router.get("/myself")
async def introduce_myself(
    walter: WalterRoasterUseCase = Depends(get_walter_roaster_use_case)
)->WalterRoasterResponse:

    return await walter.introduce_myself(
        WalterRoasterSchema(
            id=2,
            name="Walter Nichols",
            memo="타이타닉의 일등 항해사, 승객 명단 관리 담당")
        )
    