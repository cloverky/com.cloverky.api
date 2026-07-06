from __future__ import annotations

from clover.apps.fridge.app.dtos.receipt_line_dto import (
    ReceiptLineQuery,
    ReceiptLineResponse,
)
from clover.apps.fridge.app.ports.input.receipt_line_use_case import ReceiptLineUseCase
from clover.apps.fridge.app.ports.output.receipt_line_repository import (
    ReceiptLineRepository,
)
from fridge.adapter.inbound.api.schemas.receipt_line_schema import ReceiptLineSchema


class ReceiptLineInteractor(ReceiptLineUseCase):
    def __init__(self, repository: ReceiptLineRepository) -> None:
        self.repository = repository

    async def get_lines(self, schema: ReceiptLineSchema) -> ReceiptLineResponse:
        return await self.repository.get_lines(
            ReceiptLineQuery(
                receipt_id=schema.receipt_id,
            )
        )
