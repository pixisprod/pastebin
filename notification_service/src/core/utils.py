from contextlib import asynccontextmanager
import asyncio

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaConnectionError

from lib.kafka.producer import AioProducer

from src.core.messaging.producer import NotificationProducer
from src.core.service import NotificationService
from src.core.codes import CodeGenerator
from src.database.DAO import TelegramChannelsDAO
from src.config import Settings


config = Settings.load()


@asynccontextmanager
async def setup_service(kafka_server: str):
    async with kafka_producer_context(kafka_server) as kafka:
        aio_producer = AioProducer(kafka)
        business_producer = NotificationProducer(aio_producer)
        code_generator = CodeGenerator(
            alphabet='abc',
            length=7,
        )
        service = NotificationService(
            code_generator=code_generator,
            producer=business_producer,
            telegram_dao=TelegramChannelsDAO(),
        )
        yield service


@asynccontextmanager
async def kafka_producer_context(kafka_server: str):
    producer = AIOKafkaProducer(bootstrap_servers=kafka_server)
    try:
        while True:
            try:
                await producer.start()
                break
            except KafkaConnectionError:
                print('Unable to connect to kafka, retrying in 5 seconds')
                await asyncio.sleep(5)
        yield producer
    finally:
        await producer.stop()
