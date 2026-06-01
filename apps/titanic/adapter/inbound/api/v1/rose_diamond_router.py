from fastapi import APIRouter

rose_diamond_router = APIRouter(prefix="/titanic/rose", tags=["rose"])


@rose_diamond_router.get("/")
async def get_rose_diamond() -> dict[str, str | bool]:
    return {
        "character": "Rose DeWitt Bukater",
        "artifact": "diamond",
        "title": "Heart of the Ocean",
        "detail": "전설의 푸른 다이아몬드 목걸이.",
        "available": True,
    }
