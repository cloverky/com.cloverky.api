from fastapi import APIRouter, Depends
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from clover.apps.titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse
from clover.apps.titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from clover.apps.titanic.dependencies.passenger_molly_scaler_provider import get_molly_scaler_use_case

'''
몰리 브라운 (Molly Brown)
당당한 '뉴 머니(New Money)': 남편의 광산 대박으로 하루아침에 엄청난 부자가 된 인물입니다. 
이 때문에 1등실의 기존 귀족층(대대로 부를 이어온 '올드 머니')에게는 은근히 무시를 당하지만, 
특유의 호탕함과 당당함으로 맞섭니다.
잭 도슨의 조력자: 1등실 저녁 식사에 초대받은 잭(레오나르도 디카프리오)이 기죽지 않도록 
자신의 아들이 입던 턱시도를 빌려주고, 식사 예절을 친절하게 알려주는 따뜻하고 정의로운 멘토 역할을 합니다.
침몰하지 않는 강인함: 타이타닉호가 침몰할 때 6호 구명보트에 탑승했으며, 
비극적인 상황 속에서도 절망하지 않고 사람들을 독려해 노를 젓게 했습니다. 
이후 구조선 카르파티아호에서도 생존자들을 헌신적으로 돌보며 역사에 남을 영웅적인 면모를 보여줍니다.
'''

molly_scaler_router = APIRouter(prefix="/titanic/molly", tags=["molly"])


@molly_scaler_router.get("/myself")
async def introduce_myself(
    molly: MollyScalerUseCase = Depends(get_molly_scaler_use_case)
) -> MollyScalerResponse :
    return await molly.introduce_myself(
        MollyScalerSchema(
            id=14,
            name="몰리 브라운 (Molly Brown)"
        )
    )
