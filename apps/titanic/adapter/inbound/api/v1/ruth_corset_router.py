from fastapi import APIRouter

ruth_corset_router = APIRouter(prefix="/titanic/ruth", tags=["ruth"])


@ruth_corset_router.get("/")
async def get_ruth_corset() -> dict[str, str | bool]:
    return {
        "character": "Ruth DeWitt Bukater",
        "artifact": "corset",
        "title": "코르셋 조이기",
        "detail": "로즈의 허리를 조여 신분과 혼인을 강요하던 빅토리아식 코르셋.",
        "available": True,
    }
