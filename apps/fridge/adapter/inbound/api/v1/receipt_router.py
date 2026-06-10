from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile

from fridge.adapter.inbound.api.schemas.mappers import to_receipt_scan_response
from fridge.adapter.inbound.api.schemas.receipt_schemas import ReceiptScanResponse
from fridge.app.ports.input.receipt_scan_use_case import ReceiptScanUseCase
from fridge.dependencies.receipt_scan import get_receipt_scan_use_case

receipt_router = APIRouter(prefix="/receipts", tags=["receipts"])

_ALLOWED_MIME = frozenset({"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"})
_MAX_BYTES = 8 * 1024 * 1024


@receipt_router.post("/scan", response_model=ReceiptScanResponse)
async def scan_receipt(
    file: UploadFile = File(..., description="영수증 사진 (저장하지 않고 파싱만)"),
    x_user_email: str = Header(..., alias="X-User-Email"),
    receipt_scan: ReceiptScanUseCase = Depends(get_receipt_scan_use_case),
) -> ReceiptScanResponse:
    content_type = (file.content_type or "").split(";")[0].strip().lower()
    if content_type not in _ALLOWED_MIME:
        raise HTTPException(
            status_code=400,
            detail="JPEG, PNG, WEBP 형식의 영수증 이미지만 업로드할 수 있습니다.",
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")
    if len(data) > _MAX_BYTES:
        raise HTTPException(status_code=400, detail="이미지는 8MB 이하여야 합니다.")

    return to_receipt_scan_response(
        await receipt_scan.scan_receipt(x_user_email, data, content_type),
    )
