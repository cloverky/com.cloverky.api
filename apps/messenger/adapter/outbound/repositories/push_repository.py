from __future__ import annotations

from messenger.adapter.outbound.orm.push_orm import PushSubscriptionOrm
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


class PushSubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, endpoint: str, p256dh: str, auth: str) -> None:
        existing = await self.session.execute(
            select(PushSubscriptionOrm).where(PushSubscriptionOrm.endpoint == endpoint)
        )
        row = existing.scalar_one_or_none()
        if row is None:
            self.session.add(PushSubscriptionOrm(endpoint=endpoint, p256dh=p256dh, auth=auth))
        else:
            row.p256dh = p256dh
            row.auth = auth
        await self.session.commit()

    async def delete(self, endpoint: str) -> None:
        await self.session.execute(
            delete(PushSubscriptionOrm).where(PushSubscriptionOrm.endpoint == endpoint)
        )
        await self.session.commit()

    async def list_all(self) -> list[tuple[str, str, str]]:
        result = await self.session.execute(select(PushSubscriptionOrm))
        return [(r.endpoint, r.p256dh, r.auth) for r in result.scalars().all()]
