import json

from lib.kafka.producer import AioProducer


class NotificationProducer:
    def __init__(self, producer: AioProducer, topic: str = 'workers'):
        self.__producer = producer
        self.__base_topic =  topic


    async def produce(
        self,
        user_id: int,
        message: str,
        channel: str,
        event: str,
    ):
        topic = f'{self.__base_topic}.{channel}'
        payload = {
            'message': message,
        }
        val = {
            'event': event,
            'payload': payload,
        }
        await self.__producer.produce(
            topic=topic,
            key=str(user_id).encode(),
            value=json.dumps(val).encode(),
        )

        