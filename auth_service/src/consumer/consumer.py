from aiokafka import AIOKafkaConsumer

from schemas_lib.auth_service.topics import AuthTopics

from src.consumer.utils import handle_record


async def consume():
    consumer = AIOKafkaConsumer(
        *AuthTopics,
        bootstrap_servers='kafka:9092',
    )
    await consumer.start()
    try:
        async for msg in consumer:
            await handle_record(msg)
    finally:
        await consumer.stop()