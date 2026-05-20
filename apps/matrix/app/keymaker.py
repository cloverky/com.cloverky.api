"""시스템 전역 API 키·환경 변수·외부 클라이언트(Gemini, OpenWeather 등)를 한곳에서 관리합니다."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def default_backend_env_path() -> Path:
    """`backend/.env` — 이 파일: `apps/matrix/app/keymaker.py` 기준."""
    return Path(__file__).resolve().parent.parent.parent.parent / ".env"


class Keymaker:
    """
    전역 키·설정 관리자.

    - `backend/.env` 로드
    - Gemini API 키 및 `GenerativeModel` 인스턴스 보관
    - OpenWeather API 키(APPID) 및 기본 지역 설정
    """

    _instance: Keymaker | None = None

    def __init__(self, env_path: Path | None = None) -> None:
        self._env_path = env_path or default_backend_env_path()
        self._dotenv_loaded = False
        self._gemini_model: Any = None
        self._gemini_model_id = "gemini-2.5-flash"

    @classmethod
    def instance(cls, env_path: Path | None = None) -> Keymaker:
        """프로세스당 하나의 Keymaker (첫 생성 시 env_path만 적용)."""
        if cls._instance is None:
            cls._instance = cls(env_path=env_path)
        return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """테스트 등에서 인스턴스를 비울 때만 사용."""
        cls._instance = None

    def load_env(self) -> None:
        """`.env`를 한 번만 로드하고, 등록된 클라이언트를 부트스트랩합니다."""
        if self._dotenv_loaded:
            return
        from dotenv import load_dotenv

        load_dotenv(self._env_path)
        self._dotenv_loaded = True
        model_from_env = (os.getenv("GEMINI_MODEL") or "").strip()
        if model_from_env:
            self._gemini_model_id = model_from_env
        self._bootstrap_gemini()

    def _bootstrap_gemini(self) -> None:
        import google.generativeai as genai

        key = (os.getenv("GEMINI_API_KEY") or "").strip()
        if not key:
            self._gemini_model = None
            return
        genai.configure(api_key=key)
        self._gemini_model = genai.GenerativeModel(self._gemini_model_id)

    def get_secret(self, name: str, default: str = "") -> str:
        """임의 환경 변수(민감 값) 조회. 필요 시 `.env` 로드를 트리거합니다."""
        self.load_env()
        return (os.getenv(name) or default).strip()

    def get_gemini_api_key(self) -> str:
        self.load_env()
        return (os.getenv("GEMINI_API_KEY") or "").strip()

    def get_gemini_model_name(self) -> str:
        return self._gemini_model_id

    def get_gemini_model(self) -> Any:
        """설정된 경우 `google.generativeai.GenerativeModel`, 없으면 `None`."""
        self.load_env()
        return self._gemini_model

    def is_gemini_ready(self) -> bool:
        self.load_env()
        return self._gemini_model is not None

    def get_openweather_api_key(self) -> str:
        """OpenWeather `appid` — `backend/.env` 의 `OPENWEATHER_API_KEY`."""
        self.load_env()
        return (os.getenv("OPENWEATHER_API_KEY") or "").strip()

    def get_openweather_default_city(self) -> str:
        self.load_env()
        return (os.getenv("OPENWEATHER_DEFAULT_CITY") or "Seoul").strip()

    def get_openweather_default_country(self) -> str:
        self.load_env()
        return (os.getenv("OPENWEATHER_DEFAULT_COUNTRY") or "KR").strip()

    def is_openweather_ready(self) -> bool:
        self.load_env()
        return bool(self.get_openweather_api_key())


def get_keymaker(env_path: Path | None = None) -> Keymaker:
    """애플리케이션 전역에서 사용할 Keymaker 싱글톤."""
    return Keymaker.instance(env_path=env_path)
