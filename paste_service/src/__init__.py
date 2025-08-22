from fastapi import APIRouter, FastAPI

from src.paste.router import router as paste_router
from src.paste.exc_handler import init_handlers as paste_exc_handlers


router = APIRouter()
router.include_router(paste_router)

def init_handlers(app: FastAPI):
    paste_exc_handlers(app)