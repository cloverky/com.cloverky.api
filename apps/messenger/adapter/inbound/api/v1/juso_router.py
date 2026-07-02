import csv
import logging
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from messenger.adapter.inbound.api.schemas.juso_schema import (
    ContactRecordSchema,
    JusoSearchResponse,
)
from messenger.app.dtos.juso_dto import (
    ContactRecord,
    ContactUploadCommand,
    JusoMessengerQuery,
    JusoSearchCommand,
)
from messenger.app.ports.input.juso_use_case import JusoUseCase
from clover.apps.messenger.dependencies.juso_provider import get_juso_use_case

logger = logging.getLogger(__name__)

"""
주소 검색기 (Juso Messenger)
행정안전부 도로명주소 API를 통해 주소를 검색하고,
Google Contacts CSV를 파싱해 연락처를 등록한다.
"""

juso_router = APIRouter(prefix="/juso", tags=["messenger"])


@juso_router.get("/search", response_model=JusoSearchResponse)
async def search(
    keyword: str,
    page: int = 1,
    count: int = 10,
    use_case: JusoUseCase = Depends(get_juso_use_case),
) -> JusoSearchResponse:
    logger.info("주소 검색 수신 — keyword: %r", keyword)
    result = await use_case.search(
        JusoSearchCommand(keyword=keyword, page=page, count=count)
    )
    return JusoSearchResponse(
        total_count=result.total_count,
        results=[vars(r) for r in result.results],
    )


@juso_router.post("/upload", summary="Google Contacts CSV 업로드")
async def upload_contacts(
    file: UploadFile = File(...),
    use_case: JusoUseCase = Depends(get_juso_use_case),
):
    raw = (await file.read()).decode("utf-8", errors="replace")
    records = _parse_contacts_csv(raw)
    result = await use_case.upload_contacts(ContactUploadCommand(records=records))
    return {"saved": result.saved, "skipped": result.skipped}


@juso_router.get("/myself")
async def introduce_myself(
    use_case: JusoUseCase = Depends(get_juso_use_case),
):
    return await use_case.introduce_myself(
        JusoMessengerQuery(id=2, name="주소 검색기 (Juso Messenger)")
    )


def _parse_contacts_csv(text: str) -> list[ContactRecord]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    records: list[ContactRecord] = []
    for row in reader:
        cleaned = {
            k.strip(): (v or "").strip() for k, v in row.items() if k is not None
        }
        try:
            schema = ContactRecordSchema.model_validate(cleaned)
        except Exception:
            continue
        records.append(
            ContactRecord(
                first_name=schema.first_name,
                middle_name=schema.middle_name,
                last_name=schema.last_name,
                phonetic_first_name=schema.phonetic_first_name,
                phonetic_middle_name=schema.phonetic_middle_name,
                phonetic_last_name=schema.phonetic_last_name,
                name_prefix=schema.name_prefix,
                name_suffix=schema.name_suffix,
                nickname=schema.nickname,
                file_as=schema.file_as,
                organization_name=schema.organization_name,
                organization_title=schema.organization_title,
                organization_department=schema.organization_department,
                birthday=schema.birthday,
                notes=schema.notes,
                photo=schema.photo,
                labels=schema.labels,
                email_1_label=schema.email_label,
                email_1_value=schema.email_value,
                phone_1_label=schema.phone_label,
                phone_1_value=schema.phone_value,
            )
        )
    return records
