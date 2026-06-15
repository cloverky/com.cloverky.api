from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.adapter.outbound.pg.receipt_pg_repository import ReceiptPgRepository
from clover.apps.fridge.app.ports.output.receipt_repository import ReceiptRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from clover.apps.fridge.app.ports.input.receipt_use_case import ReceiptUseCase
from clover.apps.fridge.app.use_cases.receipt_interactor import ReceiptInteractor


def get_receipt_repository(
        db: AsyncSession = Depends(get_db)
) -> ReceiptPgRepository:
        return ReceiptPgRepository(session=db)

def get_receipt_use_case(
        repository: ReceiptRepository = Depends(get_receipt_repository)
) -> ReceiptUseCase:
        return ReceiptInteractor(repository=repository)
