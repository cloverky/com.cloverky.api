import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from messenger.adapter.inbound.api.schemas.mail_schema import (
    MailInboxItemResponse,
    MailInboxListResponse,
    MailInboxWebhookRequest,
)
from messenger.adapter.outbound.push.web_push_sender import send_push
from messenger.adapter.outbound.repositories.push_repository import PushSubscriptionRepository
from messenger.app.dtos.mail_dto import MailInboxReceiveCommand
from messenger.app.ports.input.mail_use_case import MailUseCase
from messenger.app.ports.input.receive_use_case import ReceiveUseCase
from messenger.dependencies.mail_provider import get_mail_use_case
from messenger.dependencies.receive_provider import get_receive_use_case
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db

logger = logging.getLogger(__name__)

receive_router = APIRouter(prefix="/mail/inbox", tags=["messenger"])


@receive_router.post("", response_model=MailInboxItemResponse)
async def receive_mail(
    req: MailInboxWebhookRequest,
    use_case: MailUseCase = Depends(get_mail_use_case),
    receive: ReceiveUseCase = Depends(get_receive_use_case),
    db: AsyncSession = Depends(get_db),
) -> MailInboxItemResponse:
    """n8n Gmail Trigger가 새 메일 수신 시 호출하는 웹훅 엔드포인트."""
    logger.info("수신 메일 저장 — from: %r, subject: %r", req.from_email, req.subject)
    item = await use_case.receive_mail(
        MailInboxReceiveCommand(
            from_email=req.from_email,
            subject=req.subject,
            body=req.body,
        )
    )

    embed_text = " ".join(filter(None, [req.subject, req.body]))

    async def _background() -> None:
        push_repo = PushSubscriptionRepository(db)
        subs = await push_repo.list_all()
        title = f"새 메일: {req.from_email}"
        push_body = req.subject or "(제목 없음)"
        await asyncio.gather(
            *[asyncio.to_thread(send_push, ep, p256dh, auth, title, push_body) for ep, p256dh, auth in subs],
            return_exceptions=True,
        )
        if embed_text:
            await receive.embed_and_store(item.id, embed_text)

    asyncio.create_task(_background())

    return MailInboxItemResponse(
        id=item.id,
        from_email=item.from_email,
        subject=item.subject,
        body=item.body,
        received_at=item.received_at,
    )


@receive_router.get("", response_model=MailInboxListResponse)
async def list_inbox(
    limit: int = Query(50, ge=1, le=200),
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> MailInboxListResponse:
    """수신 메일함 목록 조회."""
    result = await use_case.list_inbox(limit=limit)
    return MailInboxListResponse(
        items=[
            MailInboxItemResponse(
                id=it.id,
                from_email=it.from_email,
                subject=it.subject,
                body=it.body,
                received_at=it.received_at,
            )
            for it in result.items
        ]
    )


@receive_router.delete("/{item_id}")
async def delete_inbox_item(
    item_id: int = Path(..., ge=1),
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> dict:
    deleted = await use_case.delete_inbox_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="메일을 찾을 수 없습니다.")
    return {"deleted": True}


@receive_router.delete("")
async def delete_all_inbox(
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> dict:
    count = await use_case.delete_all_inbox()
    return {"deleted": count}
