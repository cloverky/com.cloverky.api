import csv
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from clover.apps.titanic.dependencies.crew_james_director import (
    get_james_director_use_case,
)
from titanic.adapter.inbound.api.schemas.crew_james_director_schema import (
    JamesDirectorSchema,
    TitanicRecordSchema,
)
from titanic.app.ports.input.crew_james_director_use_case import JamesDirectorUseCase

"""
 james_director_router.py
 전설적인 흥행작 <타이타닉>을 연출하여
 "내가 세상의 왕이다!"를 외친 제임스 카메론 감독의 라우터
 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을
 고증한 아키텍처의 총괄 디렉터 역할 수행
"""
james_director_router = APIRouter(prefix="/james", tags=["james"])


@james_director_router.get("/myself")
async def introduce_myself(
    james: JamesDirectorUseCase = Depends(get_james_director_use_case),
):
    return await james.introduce_myself(
        JamesDirectorSchema(id=6, name="제임스 카메론 (James Carmeron)")
    )


@james_director_router.post("/upload", summary="타이타닉 승객 명단 CSV 파일 업로드")
async def upload_titanic_file(
    file: UploadFile = File(...),
    james: JamesDirectorUseCase = Depends(get_james_director_use_case),
):
    result = await james.upload_titanic_file(
        _parse_csv((await file.read()).decode("utf-8", errors="replace"))
    )
    return {"count": result.get("saved", 0)}


def _parse_csv(text: str) -> list[TitanicRecordSchema]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")
    return [
        TitanicRecordSchema.model_validate(
            {k.strip(): v for k, v in row.items() if k is not None}
        )
        for row in reader
    ]
