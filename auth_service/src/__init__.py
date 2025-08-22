from fastapi import APIRouter, FastAPI

from src.auth.router import router as auth_router
from src.auth.exc_handlers import init_handlers as auth_exc_handlers


router = APIRouter()
router.include_router(auth_router)

def init_exc_handlers(app: FastAPI):
    auth_exc_handlers(app)