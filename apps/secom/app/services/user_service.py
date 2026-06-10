import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.utils.auth_password import verify_password
from models.user import User
from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import LoginResultSchema, LoginSchema, UserSchema
from secom.app.utils.log_helper import log_login_layer, log_save_user_layer

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self) -> None:
        self._user_repository = UserRepository()

    async def save_user(self, db: AsyncSession, user_schema: UserSchema) -> User:
        log_save_user_layer("Service", user_schema)
        logger.info("[Service] → Repository.save_user 호출 (Neon DB)")

        if await self._user_repository.find_by_username(db, user_schema.username):
            raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")

        existing_email = await self._user_repository.find_by_email_address(
            db,
            user_schema.email,
        )
        if existing_email:
            raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

        user = await self._user_repository.save_user(db, user_schema)
        logger.info("[Service] save_user 완료 — id=%s", user.id)
        return user

    async def login_user(
        self,
        db: AsyncSession,
        login_schema: LoginSchema,
    ) -> LoginResultSchema:
        log_login_layer("Service", login_schema)
        logger.info("[Service] → Repository.find_by_email 호출 (Neon DB)")
        user = await self._user_repository.find_by_email(db, login_schema)

        if not user:
            logger.info("[Service] 로그인 실패 — 등록되지 않은 email=%r", login_schema.email)
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        if not verify_password(login_schema.password, user.password_hash):
            logger.info("[Service] 로그인 실패 — 비밀번호 불일치 username=%r", user.username)
            raise HTTPException(
                status_code=401,
                detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            )

        logger.info(
            "[Service] 비밀번호 검증 성공 — username=%r email=%r role=%r",
            user.username,
            user.email,
            user.role,
        )
        return LoginResultSchema(
            username=user.username,
            name=user.name,
            email=user.email,
            role=user.role,
        )
