from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.app.ports.output.user_repository import UserDto, UserRepository
from models.user import User


class UserPgRepository(UserRepository):

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> UserDto:
        e = email.strip().lower()
        if not e or "@" not in e:
            raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
        result = await self._session.execute(
            select(User).where(func.lower(User.email) == e).limit(1),
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="등록된 회원이 아닙니다. 로그인해 주세요.")
        return UserDto(
            id=user.id,
            email=user.email,
            default_storage=(user.default_storage or "냉장").strip(),
        )
