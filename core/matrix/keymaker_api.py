"""Keymaker — API 키 관리 및 외부 서비스 클라이언트 팩토리."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_BACKEND_ROOT / ".env")


class Keymaker:
    def is_gemini_ready(self) -> bool:
        return bool(os.getenv("GEMINI_API_KEY", "").strip())

    def get_gemini_client(self):
        from google import genai

        return genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))

    def is_openweather_ready(self) -> bool:
        return bool(os.getenv("OPENWEATHER_API_KEY", "").strip())

    def get_openweather_api_key(self) -> str:
        return os.getenv("OPENWEATHER_API_KEY", "")

    def get_openweather_default_city(self) -> str:
        return os.getenv("OPENWEATHER_DEFAULT_CITY", "Seoul")

    def get_openweather_default_country(self) -> str:
        return os.getenv("OPENWEATHER_DEFAULT_COUNTRY", "KR")


@lru_cache(maxsize=1)
def get_keymaker() -> Keymaker:
    return Keymaker()
