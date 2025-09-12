import asyncio
from contextlib import asynccontextmanager

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

from lib.kafka.producer import AioProducer

from src.core.messaging.producer import PasteProducer
from src.core.service import PasteService
from src.database.PasteDAO import PasteDAO
from src.config import Settings


config = Settings.load()


def get_user_id_from_payload(payload: dict) -> int:
    return int(payload.get('sub'))


@asynccontextmanager
async def aiokafka_context(server: str):
    producer = AIOKafkaProducer(bootstrap_servers=server)
    try:
        while True:
            try:
                await producer.start()
                break
            except KafkaConnectionError:
                print('Unable to connect to kafka retrying in 5 seconds..')
                await asyncio.sleep(5)
        yield producer
    finally:
        await producer.stop()


@asynccontextmanager
async def setup_service():
    kafka_server = f'{config.kafka.server}:{config.kafka.server_port}'
    async with aiokafka_context(server=kafka_server) as producer:
        paste_producer = PasteProducer(
            producer=AioProducer(
                producer=producer
            ),
            base_topic='paste.events',
        )
        paste_dao = PasteDAO()
        service = PasteService(
            paste_dao=paste_dao,
            producer=paste_producer,
        )
        yield service