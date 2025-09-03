import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.utils import setup_consumer
from src.config import Settings


config = Settings.load()
kafka_server = f'{config.kafka.server}:{config.kafka.server_port}'


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    consumer = setup_consumer(kafka_server)
    loop.create_task(consumer.consume())
    print('Consumer SET')
    yield


app = FastAPI(
    lifespan=lifespan,
)