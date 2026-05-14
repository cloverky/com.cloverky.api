import json
from pathlib import Path

import pandas as pd

_DATA_DIR = Path(__file__).resolve().parent
_CSV_PATH = _DATA_DIR / "Titanic-Dataset.csv"


class WalterReader:
    def __init__(self):
        pass

    def get_full_data(self):
        return pd.read_csv(_CSV_PATH)

    def get_data(self):
        df = self.get_full_data()
        # 인덱스 1번 행만 반환 (DataFrame 형태 유지)
        return df.iloc[[0]].astype(object).where(df.iloc[[0]].notna(), None)

    def get_count(self):
        df = self.get_full_data()
        # 전체 승객 수 반환
        return len(df)

    def get_count_survived(self):
        df = self.get_full_data()
        # Survived가 1인 승객 수 반환
        return int((df["Survived"] == 1).sum())

    def get_count_not_survived(self):
        df = self.get_full_data()
        # Survived가 0인 승객 수 반환
        return int((df["Survived"] == 0).sum())