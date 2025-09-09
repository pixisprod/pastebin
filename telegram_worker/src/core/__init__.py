from fastapi import APIRouter

from .router import router as core_router


api_router = APIRouter()
api_router.include_router(core_router)