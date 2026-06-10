from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.utils.auth_password import hash_password
from models.user import User
from secom.app.schemas.user_schema import LoginSchema, UserSchema

logger = logging.getLogger(__name__)


class UserRepository:

    async def find_by_username(self, db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).where(User.username == username).limit(1))
        return result.scalar_one_or_none()

    async def find_by_email_address(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email).limit(1))
        return result.scalar_one_or_none()

    async def find_by_email(self, db: AsyncSession, login_schema: LoginSchema) -> User | None:
        result = await db.execute(
            select(User).where(User.email == login_schema.email).limit(1),
        )
        return result.scalar_one_or_none()

    async def save_user(self, db: AsyncSession, user_schema: UserSchema) -> User:
        user = User(
            username=user_schema.username.strip(),
            name=user_schema.name.strip(),
            email=user_schema.email.strip(),
            password_hash=hash_password(user_schema.password),
            role=user_schema.role.strip(),
            agree_terms=user_schema.agree_terms,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info("[Repository] save_user 완료 — id=%s username=%r", user.id, user.username)
        return user
