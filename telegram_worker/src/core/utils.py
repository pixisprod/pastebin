from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer
from httpx import AsyncClient

from src.core.messaging.consumer import TelegramConsumer
from src.core.ngrok.manager import NgrokManager


def setup_consumer(kafka_server: str) -> TelegramConsumer:
    consumer = TelegramConsumer(
        consumer=AIOKafkaConsumer(
            'workers.telegram',
            bootstrap_servers=kafka_server,
        ),
    )
    return consumer


@asynccontextmanager
async def ngrok_manager(ngrok_api_url: str):
    manager = NgrokManager(
        http_client=AsyncClient(),
        ngrok_api_url=ngrok_api_url,
    )
    try:
        yield manager
    finally:
        await manager.close()