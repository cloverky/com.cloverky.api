from fastapi import APIRouter

andrews_blueprint_router = APIRouter(prefix="/titanic/andrews", tags=["andrews"])


@andrews_blueprint_router.get("/")
async def get_andrews_blueprint() -> dict[str, str | bool]:
    return {
        "character": "Thomas Andrews",
        "artifact": "blueprint",
        "title": "RMS Titanic 설계 도면",
        "detail": "선체·격실·승객 동선을 담은 설계 청사진.",
        "available": True,
    }
