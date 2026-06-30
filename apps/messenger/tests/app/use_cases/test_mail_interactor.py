from unittest.mock import AsyncMock, MagicMock

import pytest
from messenger.app.dtos.mail_dto import MailCommand, MailResult
from messenger.app.use_cases.mail_interactor import MailInteractor

from star_craft.domain.ontology.mail.mail_taxonomy import EmailType


@pytest.mark.asyncio
async def test_send_mail_returns_success():
    mock_orchestrator = MagicMock()
    mock_orchestrator.compose_and_send = AsyncMock(return_value=None)

    interactor = MailInteractor(orchestrator=mock_orchestrator)
    cmd = MailCommand(
        to="rx@example.com",
        subject="테스트",
        context="안녕하세요",
        email_type=EmailType.NOTIFICATION,
    )

    result: MailResult = await interactor.send_mail(cmd)

    assert result.success is True
    assert "rx@example.com" in result.message
    mock_orchestrator.compose_and_send.assert_awaited_once_with(
        to="rx@example.com",
        subject="테스트",
        context="안녕하세요",
        email_type=EmailType.NOTIFICATION,
    )
