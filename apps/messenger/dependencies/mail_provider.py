from fastapi import Depends
from messenger.adapter.outbound.n8n.n8n_mail_gateway import N8nMailGateway
from messenger.adapter.outbound.repositories.mail_repository import MailPgRepository
from messenger.app.ports.input.mail_use_case import MailUseCase
from messenger.app.ports.output.mail_repository_port import MailRepositoryPort
from messenger.app.use_cases.mail_interactor import MailInteractor
from sqlalchemy.ext.asyncio import AsyncSession

from clover.core.matrix.grid_oracle_database_manager import get_db
from core.lol.t1_mid_faker_orchestrator import get_faker_orchestrator
from star_craft.app.use_cases.mail_orchestrator import MailOrchestrator


def get_mail_repository(
    db: AsyncSession = Depends(get_db),
) -> MailRepositoryPort:
    return MailPgRepository(session=db)


def get_mail_use_case(
    repository: MailRepositoryPort = Depends(get_mail_repository),
) -> MailUseCase:
    orchestrator = MailOrchestrator(
        gateway=N8nMailGateway(),
        llm=get_faker_orchestrator(),
    )
    return MailInteractor(orchestrator=orchestrator, repository=repository)
