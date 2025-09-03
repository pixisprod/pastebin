from aiokafka import AIOKafkaConsumer

from src.core.messaging.consumer import TelegramConsumer


def setup_consumer(kafka_server: str):
    consumer = TelegramConsumer(
        consumer=AIOKafkaConsumer(
            'workers.telegram',
            bootstrap_servers=kafka_server,
        ),
    )
    return consumer