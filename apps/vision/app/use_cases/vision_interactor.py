from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from vision.app.ports.input.vision_use_case import VisionUseCase
from vision.app.ports.output.vision_port import VisionPort

logger = logging.getLogger(__name__)

S3_BUCKET = os.getenv("S3_BUCKET", "cloverky.cloud-219366469305-ap-northeast-2-an")
S3_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")


class VisionInteractor(VisionUseCase):
    def __init__(self, repository: VisionPort) -> None:
        self._repository = repository
        self._s3 = boto3.client("s3", region_name=S3_REGION)

    async def introduce_myself(self, query):
        pass

    async def upload_image(self, filename: str, content: bytes, content_type: str) -> str:
        ext = filename.rsplit(".", 1)[-1].lower()
        date_prefix = datetime.utcnow().strftime("%Y/%m/%d")
        key = f"images/{date_prefix}/{uuid.uuid4().hex}.{ext}"

        try:
            self._s3.put_object(
                Bucket=S3_BUCKET,
                Key=key,
                Body=content,
                ContentType=content_type,
            )
            logger.info("[Vision] S3 업로드 완료 — bucket=%s key=%s", S3_BUCKET, key)
        except (BotoCoreError, ClientError) as e:
            logger.error("[Vision] S3 업로드 실패 — %s", e)
            raise

        return key
