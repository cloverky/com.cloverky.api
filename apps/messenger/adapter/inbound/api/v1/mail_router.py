import logging

from fastapi import APIRouter, Depends
from messenger.adapter.inbound.api.schemas.mail_schema import (
    MailRequest,
    MailResponse,
)
from messenger.app.dtos.mail_dto import MailCommand, MailMessengerQuery
from messenger.app.ports.input.mail_use_case import MailUseCase
from messenger.dependencies.mail import get_mail_use_case

logger = logging.getLogger(__name__)

"""
메신저 (Mail Messenger)
Exaone LLM이 내용을 작성하고 n8n 웹훅을 통해 Gmail로 발송하는 메일 서비스.
"""

mail_router = APIRouter(prefix="/mail", tags=["messenger"])


@mail_router.post("", response_model=MailResponse)
async def send_mail(
    req: MailRequest,
    use_case: MailUseCase = Depends(get_mail_use_case),
) -> MailResponse:
    logger.info("메일 발송 수신 — to: %r, subject: %r", req.to, req.subject)
    result = await use_case.send_mail(
        MailCommand(
            to=req.to,
            subject=req.subject,
            context=req.context,
            email_type=req.email_type,
        )
    )
    return MailResponse(success=result.success, message=result.message)


@mail_router.get("/myself")
async def introduce_myself(
    use_case: MailUseCase = Depends(get_mail_use_case),
):
    return await use_case.introduce_myself(
        MailMessengerQuery(id=1, name="메신저 (Mail Messenger)")
    )
