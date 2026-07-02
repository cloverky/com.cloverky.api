from messenger.adapter.outbound.orm.mail_orm import MailInboxOrm
from messenger.app.ports.output.receive_port import ReceiveRepositoryPort
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


class ReceivePgRepository(ReceiveRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def update_embedding(self, mail_id: int, embedding: list[float]) -> None:
        stmt = (
            update(MailInboxOrm)
            .where(MailInboxOrm.id == mail_id)
            .values(embedding=embedding)
        )
        await self._session.execute(stmt)
        await self._session.commit()
