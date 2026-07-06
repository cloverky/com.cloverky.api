import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.dependencies.vision_provider import get_vision_use_case
from vision.dependencies.face_train_provider import get_face_train_use_case
from vision.app.ports.input.face_train_use_case import FaceTrainUseCase

logger = logging.getLogger(__name__)

"""
비전 (Vision)
이미지 기반 AI 파이프라인.
"""

vision_router = APIRouter(prefix="/vision", tags=["vision"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}


@vision_router.get("/myself")
async def introduce_myself():
    return {"id": 1, "name": "Vision", "role": "이미지 기반 AI 파이프라인"}


@vision_router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    use_case: VisionUseCase = Depends(get_vision_use_case),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="JPG 또는 PNG 파일만 업로드 가능합니다.")

    content = await file.read()
    key = await use_case.upload_image(
        filename=file.filename or "upload",
        content=content,
        content_type=file.content_type,
    )
    return {"key": key, "bucket": "cloverky.cloud-219366469305-ap-northeast-2-an"}


@vision_router.post("/detect")
async def detect_face(
    file: UploadFile = File(...),
    use_case: FaceTrainUseCase = Depends(get_face_train_use_case),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="JPG 또는 PNG 파일만 업로드 가능합니다.")

    content = await file.read()
    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    detections = await use_case.detect(tmp_path)
    Path(tmp_path).unlink(missing_ok=True)
    return detections
