from fastapi import APIRouter, FastAPI

from src.core.router import router as paste_router
from src.core.exc_handler import init_handlers as paste_exc_handlers


router = APIRouter()
router.include_router(paste_router)

def init_handlers(app: FastAPI):
    paste_exc_handlers(app)