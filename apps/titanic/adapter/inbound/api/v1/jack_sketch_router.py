from fastapi import APIRouter

jack_sketch_router = APIRouter(prefix="/titanic/jack", tags=["jack"])


@jack_sketch_router.get("/")
async def get_jack_sketch() -> dict[str, str | bool]:
    return {
        "character": "Jack Dawson",
        "artifact": "sketch",
        "title": "Rose의 초상 스케치",
        "detail": "1등급 객실에서 그린 연필 드로잉.",
        "available": True,
    }
