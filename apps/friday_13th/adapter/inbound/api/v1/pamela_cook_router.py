from fastapi import APIRouter
from friday13th.app.ports.input.pamela_cook_use_case import PamelaCookUseCase

pamela_cook_router = APIRouter(prefix="/friday13th/pamela", tags=["pamela"])

@pamela_cook_router.get("/")
async def get_pamela_cook():
    return {"message": "Hello, Pamela Cook!"}
