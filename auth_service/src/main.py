import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from eventhub.kafka.producer.Producer import Producer

from src.database.core import create_tables
from src.database.UserDAO import UserDAO
from src import router, init_exc_handlers
from src.auth.AuthService import AuthService
from src.config import Settings


config = Settings.load()


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    kafka_producer = Producer(loop, config.kafka.server)
    auth_service = AuthService(user_dao=UserDAO(), kafka_producer=kafka_producer)
    await auth_service.kafka_producer.start()
    await create_tables()
    yield {config.app.service_state_key: auth_service}
    await auth_service.kafka_producer.stop()


app = FastAPI(
    title='[pastebin] Auth Service',
    lifespan=lifespan,
)


init_exc_handlers(app)
app.include_router(router)

