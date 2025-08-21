import asyncio
from contextlib import asynccontextmanager, AsyncExitStack

from aiokafka.errors import KafkaConnectionError

from eventhub.kafka.producer.Producer import Producer
from eventhub.avro.SRAvroCodec import SRAvroCodec
from eventhub.confluent.ConfluentSRClient import ConfluentSRClient

from src.auth.service import AuthService
from src.auth.UserEventsPublisher import UserEventsPublisher
from src.auth.security.bcrypt import get_bcrypt_hasher
from src.database.UserDAO import UserDAO
from src.config import Settings


async def safe_start_kafka_producer(producer: Producer) -> None:
    while True:
        try:
            await producer.start()
            break
        except KafkaConnectionError:
            print('(Kafka) Connection failed, retrying in 5 seconds..')
            await asyncio.sleep(5)


@asynccontextmanager
async def schema_registry_context(server: str):
    try:
        sr_client = ConfluentSRClient(server)
        yield sr_client
    finally:
        await sr_client.close()


@asynccontextmanager
async def kafka_producer_context(loop: asyncio.AbstractEventLoop, server: str):
    producer = Producer(loop, server)
    try:
        await safe_start_kafka_producer(producer)
        yield producer
    finally:
        await producer.stop()
        

@asynccontextmanager
async def setup_auth_service(
    loop: asyncio.AbstractEventLoop,
    config: Settings,
):
    async with AsyncExitStack() as stack:
        schemas_registry = await stack.enter_async_context(
            schema_registry_context(server=config.avro.SR_server)
        )
        kafka_producer = await stack.enter_async_context(
            kafka_producer_context(loop, config.kafka.server)
        )
        event_publisher = UserEventsPublisher(
            kafka_producer=kafka_producer,
            avro_codec=SRAvroCodec(schemas_registry),
            sr_client=schemas_registry,
        )
        auth_service = AuthService(
            user_dao=UserDAO(),
            hasher=await get_bcrypt_hasher(),
            event_publisher=event_publisher,
        )
        yield auth_service