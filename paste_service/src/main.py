import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_tables, drop_tables
from src.KafkaConsumer import KafkaConsumer
from src import router, init_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    consumer = KafkaConsumer.load()
    consumer_task = asyncio.create_task(consumer.start_consuming())
    yield
    await drop_tables()

app = FastAPI(
    title='[pastebin] Paste Service',
    lifespan=lifespan
)

init_handlers(app)
app.include_router(router)