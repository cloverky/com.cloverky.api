from fastapi import APIRouter

jason_mask_router = APIRouter(prefix="/friday13th/jason", tags=["jason"])


@jason_mask_router.get("/")
async def get_jason_mask():
    return {"message": "Hello, Jason Mask!"}
