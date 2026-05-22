"""영수증 촬영 → 파싱(이미지 미저장) → inventory 등록."""

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from fridge.models.database import get_db
from fridge.schemas.receipt_schema import ReceiptScanResponse
from fridge.services.receipt_service import ReceiptService

router = APIRouter(prefix="/receipts", tags=["receipts"])

_ALLOWED_MIME = frozenset({"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"})
_MAX_BYTES = 8 * 1024 * 1024


@router.post("/scan", response_model=ReceiptScanResponse)
async def scan_receipt(
    file: UploadFile = File(..., description="영수증 사진 (저장하지 않고 파싱만)"),
    x_user_email: str = Header(..., alias="X-User-Email"),
    db: AsyncSession = Depends(get_db),
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

    service = ReceiptService()
    return await service.scan_image(db, x_user_email, data, content_type)
