from __future__ import annotations

import os

from fastapi import APIRouter, Depends
from messenger.adapter.outbound.repositories.push_repository import PushSubscriptionRepository
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db

push_router = APIRouter(prefix="/push", tags=["messenger"])


class PushSubscribeRequest(BaseModel):
    endpoint: str
    p256dh: str
    auth: str


@push_router.get("/vapid-public-key")
async def get_vapid_public_key() -> dict:
    return {"publicKey": os.getenv("VAPID_PUBLIC_KEY", "")}


@push_router.post("/subscribe")
async def subscribe(req: PushSubscribeRequest, db: AsyncSession = Depends(get_db)) -> dict:
    repo = PushSubscriptionRepository(db)
    await repo.save(req.endpoint, req.p256dh, req.auth)
    return {"subscribed": True}


@push_router.post("/unsubscribe")
async def unsubscribe(req: PushSubscribeRequest, db: AsyncSession = Depends(get_db)) -> dict:
    repo = PushSubscriptionRepository(db)
    await repo.delete(req.endpoint)
    return {"unsubscribed": True}
