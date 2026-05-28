import csv
import io
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.app.ports.input.james_use_case import JamesUseCase

logger = logging.getLogger(__name__)

james_router = APIRouter(prefix="/titanic/james", tags=["james"])
james_use_case = JamesUseCase()

_REQUIRED_COLUMNS = (
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
)

# /titanic/james/upload 엔드포인트: Titanic
@james_router.post("/upload")
async def upload_titanic_csv(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        logger.warning("[James] CSV 업로드 거부 — csv가 아닌 파일: %r", file.filename)
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    logger.info("[James] CSV 업로드 시작 — filename=%r", file.filename)

    raw = await file.read()
    logger.info("[James] CSV 읽기 완료 — size=%d bytes", len(raw))
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="UTF-8 CSV 파일만 지원합니다.") from exc

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    missing = [col for col in _REQUIRED_COLUMNS if col not in reader.fieldnames]
    if missing:
        logger.warning(
            "[James] CSV 헤더 오류 — 누락 컬럼: %s",
            ", ".join(missing),
        )
        raise HTTPException(
            status_code=400,
            detail=f"필수 컬럼이 누락되었습니다: {', '.join(missing)}",
        )

    rows = []
    for row in reader:
        normalized = dict(row)
        normalized["gender"] = normalized.pop("Sex", "")
        rows.append(normalized)

    logger.info("[James] CSV 파싱 완료 — rows=%d, columns=%s", len(rows), reader.fieldnames)

    try:
        result = await james_use_case.execute(db, rows)
    except RuntimeError as exc:
        logger.exception("[James] 업로드 처리 실패 — 서비스 일시 장애")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("[James] 업로드 처리 실패 — 알 수 없는 오류")
        raise HTTPException(status_code=500, detail="CSV 처리 중 서버 오류가 발생했습니다.") from exc

    logger.info(
        "[James] CSV 업로드 처리 완료 — filename=%r, saved=%s",
        file.filename,
        result.get("count"),
    )

    return {
        "message": "Neon DB 전송 완료",
        "count": result["count"],
        "columns": [*reader.fieldnames, "gender"],
        "rows": result["rows"],
    }



