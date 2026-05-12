import json
from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent
_CSV_PATH = _DATA_DIR / "한국도로공사_교통사고통계_20241231.csv"


class DoroReader:
    def __init__(self):
        pass

    def _read_csv_with_fallback_encoding(self):
        # 공공데이터 CSV는 cp949/euc-kr로 저장되는 경우가 많아 utf-8 실패 시 순차 시도한다.
        encodings = ("utf-8", "cp949", "euc-kr")
        last_error = None
        for encoding in encodings:
            try:
                return pd.read_csv(_CSV_PATH, encoding=encoding)
            except UnicodeDecodeError as error:
                last_error = error
        raise UnicodeDecodeError(
            "utf-8",
            b"",
            0,
            1,
            f"Failed to decode {_CSV_PATH.name} with encodings {encodings}: {last_error}",
        )

    def get_data(self):
        df = self._read_csv_with_fallback_encoding()
        # 인덱스 1번 행만 반환 (DataFrame 형태 유지)
        return df.iloc[[1]].astype(object).where(df.iloc[[1]].notna(), None)