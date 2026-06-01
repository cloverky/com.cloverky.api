from fastapi import APIRouter

cal_pistol_router = APIRouter(prefix="/titanic/cal", tags=["cal"])


@cal_pistol_router.get("/")
async def get_cal_pistol() -> dict[str, str | bool]:
    return {
        "character": "Caledon Hockley",
        "artifact": "pistol",
        "title": "칼의 권총",
        "detail": "선실 추격 장면에 등장한 콜트 리볼버.",
        "available": True,
    }
