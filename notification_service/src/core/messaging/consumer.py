import json

from aiokafka import AIOKafkaConsumer, ConsumerRecord

from lib.kafka.consumer.aioconsumer import AioConsumer

from src.core.messaging.producer import NotificationProducer


class NotificationConsumer:
    def __init__(self, consumer: AIOKafkaConsumer, producer: NotificationProducer):
        self.__low_level_consumer = consumer
        self.__producer = producer
        self.__consumer = AioConsumer(self.__low_level_consumer)
        

        @self.__consumer.handler('published')
        async def _(msg: ConsumerRecord):
            decoded = json.loads(msg.value)
            payload = decoded['payload']
            user_id = int(msg.key.decode())
            paste_id = payload['paste_id']
            public_url = payload['public_url']
            message = (
                f'Your paste with ID: {paste_id} was published!'
                f'Public url: {public_url}'
            )
            await self.__producer.produce(
                user_id=user_id,
                message=message,
                channel='telegram',
                event='sent',
            )


    async def consume(self):
        await self.__consumer.consume()