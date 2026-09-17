from fastapi import APIRouter
from src.dto.ai_schema import BlogRequest
from src.controller import ai_controller
ai_router = APIRouter(prefix="/ai",tags=["AI"])


@ai_router.post("/blog/generate")
async def generate_blog(request:BlogRequest):
    print(request)
    response = await ai_controller.llm_invoke(request)
    return response

