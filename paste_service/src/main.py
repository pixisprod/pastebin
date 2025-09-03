from aiokafka import AIOKafkaConsumer
import asyncio


from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.core import create_tables
from src import router, init_handlers
from src.config import Settings
from src.core.utils import setup_service


config = Settings.load()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    async with setup_service() as service:
        yield {config.app.service_state_key: service}

app = FastAPI(
    title='[pastebin] Paste Service',
    lifespan=lifespan,
    root_path='/paste'
)

init_handlers(app)
app.include_router(router)