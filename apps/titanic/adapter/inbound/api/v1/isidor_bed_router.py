from fastapi import APIRouter

isidor_bed_router = APIRouter(prefix="/titanic/isidor", tags=["isidor"])


@isidor_bed_router.get("/")
async def get_isidor_bed() -> dict[str, str | bool]:
    return {
        "character": "Isidor & Ida Straus",
        "artifact": "bed",
        "title": "함께한 마지막 침실",
        "detail": "구명보트를 거절하고 부부가 함께한 순간을 상징.",
        "available": True,
    }
