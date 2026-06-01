from fastapi import APIRouter

hartley_violin_router = APIRouter(prefix="/titanic/hartley", tags=["hartley"])


@hartley_violin_router.get("/")
async def get_hartley_violin() -> dict[str, str | bool]:
    return {
        "character": "Wallace Hartley",
        "artifact": "violin",
        "title": "침몰 직전의 바이올린",
        "detail": "밴드마스터가 연주하던 마지막 선율.",
        "available": True,
    }
