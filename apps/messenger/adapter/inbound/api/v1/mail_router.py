import logging

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from messenger.adapter.inbound.api.schemas.mail_schema import (
    MailInboxItemResponse,
    MailInboxListResponse,
    MailInboxWebhookRequest,
    MailRequest,
    MailResponse,
)
from messenger.app.dtos.mail_dto import (
    MailCommand,
    MailInboxReceiveCommand,
    MailMessengerQuery,
)
from messenger.app.ports.input.mail_use_case import MailUseCase
from messenger.dependencies.mail import get_mail_use_case

logger = logging.getLogger(__name__)

mail_router = APIRouter(prefix="/mail", tags=["messenger"])


@mail_router.post("", response_model=MailResponse)
async def send_mail(
    req: MailRequest,
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> MailResponse:
    logger.info("메일 발송 — to: %r, subject: %r", req.to, req.subject)
    result = await use_case.send_mail(
        MailCommand(
            to=req.to,
            subject=req.subject,
            context=req.context,
            email_type=req.email_type,
        )
    )
    return MailResponse(success=result.success, message=result.message)


@mail_router.post("/inbox", response_model=MailInboxItemResponse)
async def receive_mail(
    req: MailInboxWebhookRequest,
    use_case: MailUseCase = Depends(get_mail_use_case),
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
    return MailInboxItemResponse(
        id=item.id,
        from_email=item.from_email,
        subject=item.subject,
        body=item.body,
        received_at=item.received_at,
    )


@mail_router.get("/inbox", response_model=MailInboxListResponse)
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


@mail_router.delete("/inbox/{item_id}")
async def delete_inbox_item(
    item_id: int = Path(..., ge=1),
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> dict:
    deleted = await use_case.delete_inbox_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="메일을 찾을 수 없습니다.")
    return {"deleted": True}


@mail_router.delete("/inbox")
async def delete_all_inbox(
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> dict:
    count = await use_case.delete_all_inbox()
    return {"deleted": count}


@mail_router.get("/myself")
async def introduce_myself(
    use_case: MailUseCase = Depends(get_mail_use_case),
):
    return await use_case.introduce_myself(
        MailMessengerQuery(id=1, name="메신저 (Mail Messenger)")
    )
