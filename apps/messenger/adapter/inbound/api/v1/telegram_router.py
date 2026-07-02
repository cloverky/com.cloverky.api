import logging
import os

from fastapi import APIRouter, Depends, HTTPException
from messenger.adapter.inbound.api.schemas.telegram_schema import (
    TelegramNotifyRequest,
    TelegramSendRequest,
    TelegramSendResponse,
)
from messenger.app.dtos.telegram_dto import TelegramMessengerQuery, TelegramSendCommand
from messenger.app.ports.input.telegram_use_case import TelegramUseCase
from clover.apps.messenger.dependencies.telegram_provider import get_telegram_use_case

_MY_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

logger = logging.getLogger(__name__)

"""
텔레그램 메신저 (Telegram Messenger)
Telegram Bot API를 통해 채팅방에 메시지를 전송한다.
TELEGRAM_BOT_TOKEN 환경변수 필요.
"""

telegram_router = APIRouter(prefix="/telegram", tags=["messenger"])


@telegram_router.post("", response_model=TelegramSendResponse)
async def send(
    req: TelegramSendRequest,
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramSendResponse:
    logger.info("텔레그램 메시지 수신 — chat_id: %r", req.chat_id)
    result = await use_case.send(
        TelegramSendCommand(chat_id=req.chat_id, text=req.text)
    )
    return TelegramSendResponse(success=result.success, message=result.message)


@telegram_router.post(
    "/notify", summary="내 텔레그램으로 알림 전송 (TELEGRAM_CHAT_ID 사용)"
)
async def notify_me(
    req: TelegramNotifyRequest,
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramSendResponse:
    if not _MY_CHAT_ID:
        raise HTTPException(
            status_code=503,
            detail="TELEGRAM_CHAT_ID 환경변수가 설정되지 않았습니다.",
        )
    result = await use_case.send(
        TelegramSendCommand(chat_id=_MY_CHAT_ID, text=req.text)
    )
    return TelegramSendResponse(success=result.success, message=result.message)


@telegram_router.get("/myself")
async def introduce_myself(
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
):
    return await use_case.introduce_myself(
        TelegramMessengerQuery(id=4, name="텔레그램 메신저 (Telegram Messenger)")
    )
