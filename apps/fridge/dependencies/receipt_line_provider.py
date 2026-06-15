from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from clover.apps.fridge.adapter.outbound.pg.receipt_line_pg_repository import ReceiptLinePgRepository
from clover.apps.fridge.app.ports.output.receipt_line_repository import ReceiptLineRepository
from clover.core.matrix.grid_oracle_database_manager import get_db
from clover.apps.fridge.app.ports.input.receipt_line_use_case import ReceiptLineUseCase
from clover.apps.fridge.app.use_cases.receipt_line_interactor import ReceiptLineInteractor


def get_receipt_line_repository(
        db: AsyncSession = Depends(get_db)
) -> ReceiptLinePgRepository:
        return ReceiptLinePgRepository(session=db)

def get_receipt_line_use_case(
        repository: ReceiptLineRepository = Depends(get_receipt_line_repository)
) -> ReceiptLineUseCase:
        return ReceiptLineInteractor(repository=repository)
