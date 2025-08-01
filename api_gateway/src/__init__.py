from fastapi import APIRouter, FastAPI

from src.auth.router import router as auth_router
from src.paste.router import router as paste_router
from src.auth.exc_handler import init_handlers as auth_exc_handlers


v1router = APIRouter(
    prefix='/v1',
)
v1router.include_router(auth_router)
v1router.include_router(paste_router)


router = APIRouter(
    prefix='/api'
)
router.include_router(v1router)

def init_handlers(app: FastAPI):
    auth_exc_handlers(app)