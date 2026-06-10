"""서울 날씨 — OpenWeather 우선, 실패 시 Open-Meteo(키 불필요) 폴백."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)

SEOUL_LAT = 37.5665
SEOUL_LON = 126.9780


def _wmo_to_openweather_icon(code: int, *, night: bool = False) -> str:
    suffix = "n" if night else "d"
    if code == 0:
        return f"01{suffix}"
    if code in (1, 2):
        return f"02{suffix}"
    if code == 3:
        return f"04{suffix}"
    if code in (45, 48):
        return "50d"
    if code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
        return "10d"
    if code in (71, 73, 75, 77, 85, 86):
        return "13d"
    if code in (95, 96, 99):
        return "11d"
    return f"03{suffix}"


def _wmo_description_ko(code: int) -> str:
    if code == 0:
        return "맑음"
    if code in (1, 2):
        return "대체로 맑음"
    if code == 3:
        return "흐림"
    if code in (45, 48):
        return "안개"
    if code in (51, 53, 55):
        return "이슬비"
    if code in (56, 57):
        return "진눈깨비"
    if code in (61, 63, 65):
        return "비"
    if code in (66, 67):
        return "진눈깨비"
    if code in (71, 73, 75):
        return "눈"
    if code in (77, 85, 86):
        return "눈보라"
    if code in (80, 81, 82):
        return "소나기"
    if code in (95, 96, 99):
        return "뇌우"
    return "흐림"


def _static_seoul_fallback() -> dict[str, Any]:
    return {
        "city": "Seoul",
        "country": "KR",
        "temp_c": 18.0,
        "feels_like_c": 18.0,
        "description": "맑음",
        "icon": "01d",
        "humidity": 55,
    }


def fetch_openweather(
    *,
    appid: str,
    city: str,
    country: str,
) -> dict[str, Any]:
    query = f"{city.strip()},{country.strip()}"
    params = urllib.parse.urlencode(
        {
            "q": query,
            "appid": appid,
            "units": "metric",
            "lang": "kr",
        },
    )
    url = f"https://api.openweathermap.org/data/2.5/weather?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    main = data["weather"][0]
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp_c": float(data["main"]["temp"]),
        "feels_like_c": float(data["main"]["feels_like"]),
        "description": main["description"],
        "icon": main["icon"],
        "humidity": int(data["main"]["humidity"]),
    }


def fetch_open_meteo_seoul() -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "latitude": SEOUL_LAT,
            "longitude": SEOUL_LON,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
            "timezone": "Asia/Seoul",
        },
    )
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.loads(resp.read().decode())
    cur = data["current"]
    code = int(cur["weather_code"])
    temp = float(cur["temperature_2m"])
    return {
        "city": "Seoul",
        "country": "KR",
        "temp_c": temp,
        "feels_like_c": temp,
        "description": _wmo_description_ko(code),
        "icon": _wmo_to_openweather_icon(code),
        "humidity": int(cur.get("relative_humidity_2m", 50)),
    }


def fetch_seoul_weather(
    *,
    openweather_appid: str | None,
    city: str = "Seoul",
    country: str = "KR",
) -> dict[str, Any]:
    """항상 dict 반환 — OpenWeather → Open-Meteo → 고정 기본값."""
    if openweather_appid:
        try:
            return fetch_openweather(appid=openweather_appid, city=city, country=country)
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.warning("OpenWeather 실패, Open-Meteo 폴백: %s", e)

    try:
        return fetch_open_meteo_seoul()
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        logger.warning("Open-Meteo 실패, 정적 폴백: %s", e)

    return _static_seoul_fallback()
