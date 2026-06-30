from messenger.app.dtos.mail_dto import (
    MailCommand,
    MailMessengerQuery,
    MailMessengerResponse,
    MailResult,
)
from messenger.app.ports.input.mail_use_case import MailUseCase
from messenger.app.ports.output.mail_repository_port import MailRepositoryPort

from star_craft.app.use_cases.mail_orchestrator import MailOrchestrator


class MailInteractor(MailUseCase):
    def __init__(
        self,
        orchestrator: MailOrchestrator,
        repository: MailRepositoryPort,
    ) -> None:
        self._orchestrator = orchestrator
        self._repository = repository

    async def send_mail(self, cmd: MailCommand) -> MailResult:
        await self._orchestrator.compose_and_send(
            to=cmd.to,
            subject=cmd.subject,
            context=cmd.context,
            email_type=cmd.email_type,
        )
        return MailResult(success=True, message=f"{cmd.to} 으로 발송 완료")

    async def introduce_myself(
        self, query: MailMessengerQuery
    ) -> MailMessengerResponse:
        return await self._repository.introduce_myself(query)
