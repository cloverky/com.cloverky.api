from fastapi import APIRouter, Depends

from clover.apps.fridge.app.dtos.user_dto import UserResponse
from clover.apps.fridge.app.ports.input.user_use_case import UserUseCase
from clover.apps.fridge.dependencies.user_provider import get_user_use_case
from fridge.adapter.inbound.api.schemas.user_schema import UserSchema

"""
사용자 (User)
냉장고 식재료 관리 서비스의 주인. default_storage 설정으로
냉장·냉동·실온 중 기본 보관장소를 지정하며, 모든 인벤토리와
영수증 데이터의 소유자 역할을 담당한다.
"""

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me")
async def get_me(user: UserUseCase = Depends(get_user_use_case)) -> UserResponse:
    return await user.get_me(
        UserSchema(
            username="cloverky",
            name="홍길동",
        )
    )
