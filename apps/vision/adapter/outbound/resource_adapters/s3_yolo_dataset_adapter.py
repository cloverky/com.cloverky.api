from __future__ import annotations

import os
import tempfile
from pathlib import Path

import boto3

from vision.app.ports.output.face_dataset_port import FaceDatasetPort

S3_BUCKET = os.getenv("S3_BUCKET", "cloverky.cloud-219366469305-ap-northeast-2-an")
S3_REGION = os.getenv("AWS_DEFAULT_REGION", "ap-northeast-2")


class S3YoloDatasetAdapter(FaceDatasetPort):
    """S3에서 data.yaml을 포함한 데이터셋을 로컬에 다운로드 후 경로를 반환한다."""

    def __init__(self, s3_prefix: str = "datasets/yolo_train/") -> None:
        self._s3_prefix = s3_prefix
        self._s3 = boto3.client("s3", region_name=S3_REGION)

    def get_dataset_config_path(self) -> str:
        tmp_dir = Path(tempfile.mkdtemp(prefix="yolo_dataset_"))
        paginator = self._s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=S3_BUCKET, Prefix=self._s3_prefix):
            for obj in page.get("Contents", []):
                key: str = obj["Key"]
                rel = key[len(self._s3_prefix):]
                local_path = tmp_dir / rel
                local_path.parent.mkdir(parents=True, exist_ok=True)
                self._s3.download_file(S3_BUCKET, key, str(local_path))

        yaml_path = tmp_dir / "data.yaml"
        if not yaml_path.exists():
            raise FileNotFoundError(f"S3에서 data.yaml을 찾을 수 없음: s3://{S3_BUCKET}/{self._s3_prefix}")
        return str(yaml_path)
