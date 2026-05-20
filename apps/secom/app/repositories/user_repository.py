import logging

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.services.auth_password import hash_password
from models.user import User
from secom.app.schemas.user_schema import LoginSchema, UserSchema
from secom.app.utils.log_helper import (
    log_login_layer,
    log_save_user_layer,
    mask_user_payload,
)

logger = logging.getLogger(__name__)


def _username_key(username: str) -> str:
    return username.strip().lower()


class UserRepository:
    """Neon Postgres users 테이블 — Repository 레이어에서 직접 접속."""

    async def find_by_username(self, db: AsyncSession, username: str) -> User | None:
        key = _username_key(username)
        result = await db.execute(
            select(User).where(func.lower(User.username) == key).limit(1),
        )
        return result.scalar_one_or_none()

    async def find_by_email_address(self, db: AsyncSession, email: str) -> User | None:
        email_key = email.strip().lower()
        result = await db.execute(
            select(User).where(func.lower(User.email) == email_key).limit(1),
        )
        return result.scalar_one_or_none()

    async def find_by_email(self, db: AsyncSession, login_schema: LoginSchema) -> User | None:
        log_login_layer("Repository", login_schema)
        email_key = login_schema.email.strip().lower()
        result = await db.execute(
            select(User).where(func.lower(User.email) == email_key).limit(1),
        )
        user = result.scalar_one_or_none()
        logger.info(
            "[Repository] find_by_email 결과 — found=%s username=%r email=%r role=%r",
            user is not None,
            getattr(user, "username", None),
            getattr(user, "email", None),
            getattr(user, "role", None),
        )
        return user

    async def save_user(self, db: AsyncSession, user_schema: UserSchema) -> User:
        """Repository 도착 시 Neon DB에 즉시 INSERT."""
        log_save_user_layer("Repository", user_schema)

        user = User(
            username=user_schema.username.strip(),
            name=user_schema.name.strip(),
            email=user_schema.email.strip(),
            password_hash=hash_password(user_schema.password),
            role=user_schema.role,
            agree_terms=user_schema.agree_terms,
        )
        db.add(user)

        try:
            await db.commit()
            await db.refresh(user)
        except IntegrityError as e:
            await db.rollback()
            logger.error(
                "[Repository] Neon DB 저장 실패 — username=%r email=%r",
                user_schema.username,
                user_schema.email,
            )
            raise HTTPException(
                status_code=400,
                detail="이미 가입된 아이디 또는 이메일입니다.",
            ) from e

        logger.info(
            "[Repository] Neon DB 저장 완료 — id=%s username=%r email=%r role=%r password=%s",
            user.id,
            user.username,
            user.email,
            user.role,
            mask_user_payload(user_schema)["password"],
        )
        return user
