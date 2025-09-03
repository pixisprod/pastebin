from contextlib import asynccontextmanager

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from lib.kafka.producer import AioProducer

from src.core.messaging.consumer import NotificationConsumer
from src.core.messaging.producer import NotificationProducer


@asynccontextmanager
async def kafka_producer_context(kafka_server: str):
    producer = AIOKafkaProducer(bootstrap_servers=kafka_server)
    try:
        await producer.start()
        yield producer
    finally:
        await producer.stop()


@asynccontextmanager
async def setup_kafka_consumer(*topics: str, kafka_server: str):
    async with kafka_producer_context(kafka_server=kafka_server) as low_producer:
        producer = NotificationProducer(
            producer=AioProducer(low_producer)
        )
        low_level_consumer = AIOKafkaConsumer(
            *topics,
            bootstrap_servers=kafka_server,
        )
        consumer = NotificationConsumer(
            consumer=low_level_consumer,
            producer=producer,
        )
        yield consumer