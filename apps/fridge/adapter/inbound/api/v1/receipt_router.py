from fastapi import APIRouter, Depends

from clover.apps.fridge.app.dtos.receipt_dto import ReceiptUploadResponse
from clover.apps.fridge.app.ports.input.receipt_use_case import ReceiptUseCase
from clover.apps.fridge.dependencies.receipt_provider import get_receipt_use_case
from fridge.adapter.inbound.api.schemas.receipt_schema import ReceiptUploadSchema

"""
영수증 업로드 (Receipt Upload)
AI OCR이 영수증 이미지를 인식하기 전 사용자가 제출하는
메타데이터를 처리한다. 매장명·구매일자·처리상태를 관리하며
영수증 상세 품목(ReceiptLine) 파싱의 진입점 역할을 담당한다.
"""

receipt_router = APIRouter(prefix="/receipt", tags=["receipt"])


@receipt_router.get("/status")
async def get_status(
    receipt: ReceiptUseCase = Depends(get_receipt_use_case),
) -> ReceiptUploadResponse:
    return await receipt.get_status(
        ReceiptUploadSchema(
            user_id=1,
            store_name="이마트",
            status="pending",
        )
    )
