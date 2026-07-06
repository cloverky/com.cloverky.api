from __future__ import annotations

from clover.apps.fridge.app.dtos.receipt_dto import ReceiptQuery, ReceiptUploadResponse
from clover.apps.fridge.app.ports.input.receipt_use_case import ReceiptUseCase
from clover.apps.fridge.app.ports.output.receipt_repository import ReceiptRepository
from fridge.adapter.inbound.api.schemas.receipt_schema import ReceiptUploadSchema


class ReceiptInteractor(ReceiptUseCase):
    def __init__(self, repository: ReceiptRepository) -> None:
        self.repository = repository

    async def get_status(self, schema: ReceiptUploadSchema) -> ReceiptUploadResponse:
        return await self.repository.get_status(
            ReceiptQuery(
                user_id=schema.user_id,
                status=schema.status,
            )
        )
