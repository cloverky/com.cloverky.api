import logging

from fastapi import APIRouter, Depends
from messenger.adapter.inbound.api.schemas.discord_schema import (
    DiscordSendRequest,
    DiscordSendResponse,
)
from messenger.app.dtos.discord_dto import DiscordMessengerQuery, DiscordSendCommand
from messenger.app.ports.input.discord_use_case import DiscordUseCase
from clover.apps.messenger.dependencies.discord_provider import get_discord_use_case

logger = logging.getLogger(__name__)

"""
디스코드 메신저 (Discord Messenger)
Discord 웹훅을 통해 채널에 메시지를 전송한다.
DISCORD_WEBHOOK_URL 환경변수 필요.
"""

discord_router = APIRouter(prefix="/discord", tags=["messenger"])


@discord_router.post("", response_model=DiscordSendResponse)
async def send(
    req: DiscordSendRequest,
    use_case: DiscordUseCase = Depends(get_discord_use_case),
) -> DiscordSendResponse:
    logger.info("디스코드 메시지 수신 — username: %r", req.username)
    result = await use_case.send(
        DiscordSendCommand(content=req.content, username=req.username)
    )
    return DiscordSendResponse(success=result.success, message=result.message)


@discord_router.get("/myself")
async def introduce_myself(
    use_case: DiscordUseCase = Depends(get_discord_use_case),
):
    return await use_case.introduce_myself(
        DiscordMessengerQuery(id=3, name="디스코드 메신저 (Discord Messenger)")
    )
