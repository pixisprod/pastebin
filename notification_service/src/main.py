from contextlib import asynccontextmanager
import asyncio

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from src.config import Settings
from src.core.messaging.consumer import NotificationConsumer
from src.database.core import create_tables, session_factory
from src.core.utils import setup_service
from src.core.router import router


config = Settings.load()
kafka_server = f'{config.kafka.server}:{config.kafka.server_port}'


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print('Database set')
    loop = asyncio.get_event_loop()
    async with setup_service(kafka_server) as service:
        low_level_consumer = AIOKafkaConsumer(
            'paste.events',
            bootstrap_servers=kafka_server,
        )
        consumer = NotificationConsumer(
            consumer=low_level_consumer,
            service=service,
            db_session_factory=session_factory,
        )
        loop.create_task(consumer.consume())
        yield {config.app.service_state_key: service}


app = FastAPI(
    lifespan=lifespan,
    title='[pastebin] Notify Service',
    root_path='/notify',
)
app.include_router(router)