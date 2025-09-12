import json

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from sqlalchemy.ext.asyncio import async_sessionmaker

from lib.kafka.consumer.aioconsumer import AioConsumer

from src.core.service import NotificationService


class NotificationConsumer:
    def __init__(
        self, 
        consumer: AIOKafkaConsumer, 
        service: NotificationService,
        db_session_factory = async_sessionmaker,
    ):
        self.__low_level_consumer = consumer
        self.__service = service
        self.__consumer = AioConsumer(self.__low_level_consumer)
        self.__db_sessions_factory = db_session_factory
        

        @self.__consumer.handler('published')
        async def _(msg: ConsumerRecord):
            decoded = json.loads(msg.value)
            payload = decoded['payload']
            user_id = int(msg.key.decode())
            paste_id = payload['paste_id']
            public_url = payload['public_url']
            async with self.__db_sessions_factory() as db:
                telegram_user_id = await self.__service.get_user_telegram(
                    db=db,
                    user_id=user_id,
                )
            message = (
                f'Your paste with ID: {paste_id} was published!\n'
                f'Public url: {public_url}'
            )
            await self.__service.send_by_telegram(
                user_id=telegram_user_id,
                message=message,
            )


    async def consume(self):
        await self.__consumer.consume()