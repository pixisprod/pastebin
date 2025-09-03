import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.core import create_tables
from src import router, init_exc_handlers
from src.auth.utils import setup_auth_service
from src.config import Settings


config = Settings.load()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    auth_service = setup_auth_service()
    yield {config.app.service_state_key: auth_service}


app = FastAPI(
    title='[pastebin] Auth Service',
    lifespan=lifespan,
    root_path='/auth'
)


init_exc_handlers(app)
app.include_router(router)

