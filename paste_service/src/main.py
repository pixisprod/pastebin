from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.core import create_tables
from src import router, init_handlers
from src.config import Settings


from src.database.PasteDAO import PasteDAO
from src.paste.service import PasteService


config = Settings.load()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield {config.app.service_state_key: PasteService(PasteDAO())}

app = FastAPI(
    title='[pastebin] Paste Service',
    lifespan=lifespan
)

init_handlers(app)
app.include_router(router)