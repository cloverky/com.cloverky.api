from fastapi import APIRouter, Depends

from clover.apps.fridge.app.dtos.receipt_line_dto import ReceiptLineResponse
from clover.apps.fridge.app.ports.input.receipt_line_use_case import ReceiptLineUseCase
from clover.apps.fridge.dependencies.receipt_line_provider import (
    get_receipt_line_use_case,
)
from fridge.adapter.inbound.api.schemas.receipt_line_schema import ReceiptLineSchema

"""
영수증 상세 품목 (Receipt Line)
AI OCR이 영수증에서 한 줄씩 인식한 품목 데이터.
raw_text로 원문을 보존하고, line_name·quantity·unit으로
파싱된 정형 데이터를 관리한다. 인벤토리 자동 등록의 소스 역할을 담당한다.
"""

receipt_line_router = APIRouter(prefix="/receipt-line", tags=["receipt-line"])


@receipt_line_router.get("/lines")
async def get_lines(
    receipt_line: ReceiptLineUseCase = Depends(get_receipt_line_use_case),
) -> ReceiptLineResponse:
    return await receipt_line.get_lines(
        ReceiptLineSchema(
            receipt_id=1,
            line_name="사과",
            quantity=3,
            unit="개",
            raw_text="사과 3개 2,990원",
        )
    )
