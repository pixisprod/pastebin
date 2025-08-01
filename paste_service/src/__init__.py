from fastapi import APIRouter, FastAPI

from src.paste.router import router as paste_router
from src.paste.exc_handler import init_handlers as paste_exc_handlers

v1router = APIRouter(prefix='/v1')
v1router.include_router(paste_router)

router = APIRouter(prefix='/api')
router.include_router(v1router)

def init_handlers(app: FastAPI):
    paste_exc_handlers(app)