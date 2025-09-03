from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI

from src.config import Settings
from src.core.utils import setup_kafka_consumer


config = Settings.load()
kafka_server = f'{config.kafka.server}:{config.kafka.server_port}'


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with setup_kafka_consumer('paste.events', kafka_server=kafka_server) as consumer:
        loop = asyncio.get_event_loop()
        loop.create_task(consumer.consume())
        yield


app = FastAPI(
    lifespan=lifespan,
    title='[pastebin] Notify Service',
)