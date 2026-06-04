from __future__ import annotations

import csv
import io
import logging
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import ValidationError
from titanic.adapter.inbound.api.schemas.james_director_schemas import (
    JAMES_DIRECTOR_CSV_COLUMNS,
    JamesDirectorUploadResponseSchema,
    TitanicRecordSchema,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor

logger = logging.getLogger(__name__)

james_director_router = APIRouter(prefix="/titanic/james", tags=["james"])


def _load_titanic_records(text: str) -> tuple[list[TitanicRecordSchema], list[str]]:
    """CSV 텍스트를 TitanicRecordSchema 목록으로 옮겨 담는다."""
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    missing = [col for col in JAMES_DIRECTOR_CSV_COLUMNS if col not in reader.fieldnames]
    if missing:
        logger.warning(
            "🍀 [James] CSV 헤더 오류 — 누락 컬럼: %s",
            ", ".join(missing),
        )
        raise HTTPException(
            status_code=400,
            detail=f"필수 컬럼이 누락되었습니다: {', '.join(missing)}",
        )

    records: list[TitanicRecordSchema] = []
    for line_no, row in enumerate(reader, start=2):
        try:
            records.append(TitanicRecordSchema.model_validate(row))
        except ValidationError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"CSV {line_no}행 데이터 형식이 올바르지 않습니다: {exc.errors()[0]['msg']}",
            ) from exc

    return records, list(reader.fieldnames)


def _to_repository_rows(records: list[TitanicRecordSchema]) -> list[dict[str, Any]]:
    return [record.model_dump() for record in records]


@james_director_router.post("/upload", response_model=JamesDirectorUploadResponseSchema)
async def upload_titanic_csv(
    file: UploadFile = File(...),
) -> JamesDirectorUploadResponseSchema:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        logger.warning("🍀 [James] CSV 업로드 거부 — csv가 아닌 파일: %r", file.filename)
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    logger.info("🍀 [James] CSV 업로드 시작 — filename=%r", file.filename)

    raw = await file.read()
    logger.info("🍀 [James] CSV 읽기 완료 — size=%d bytes", len(raw))
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="UTF-8 CSV 파일만 지원합니다.") from exc

    titanic_records, fieldnames = _load_titanic_records(text)

    # 레코드 목록 상위 5줄만 출력 (실제 서비스에서는 제거)
    for index, record in enumerate(titanic_records[:5], start=1):
        logger.info(
            "🎀 [제임스 라우터] 업로드된 csv 파일에서 스키마로 옮겨진 상위 5개 레코드 %d/5 — %s",
            index,
            record.model_dump(),
        )
    rows = _to_repository_rows(titanic_records)
    use_case : JamesDirectorUseCase = JamesDirectorInteractor()

    logger.info(
        "🍀 [James] CSV 파싱 완료 — rows=%d, columns=%s",
        len(titanic_records),
        fieldnames,
    )

    try:
        result = await use_case.receive_uploaded_records(rows)
    except RuntimeError as exc:
        logger.exception("🍀 [James] 업로드 처리 실패 — 서비스 일시 장애")
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("🍀 [James] 업로드 처리 실패 — 알 수 없는 오류")
        raise HTTPException(status_code=500, detail="CSV 처리 중 서버 오류가 발생했습니다.") from exc

    return JamesDirectorUploadResponseSchema(
        message="Neon DB 전송 완료",
        count=result["count"],
        columns=[*fieldnames, "gender"],
        rows=result["rows"],
    )
