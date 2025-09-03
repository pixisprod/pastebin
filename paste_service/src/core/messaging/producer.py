import json

from lib.kafka.producer import AioProducer


class PasteProducer:
    def __init__(self, producer: AioProducer, base_topic: str = 'paste'):
        self.__producer = producer
        self.__base_topic = base_topic

    
    async def __produce(
        self,
        user_id: int,
        event: str,
        payload: dict,
    ) -> None:
        value = {
            'event': event,
            'payload': payload,
        }
        encoded = json.dumps(value).encode()
        await self.__producer.produce(
            topic=self.__base_topic,
            key=str(user_id).encode(),
            value=json.dumps(value).encode(),
        )


    async def paste_published(
        self,
        user_id: int,
        paste_id: int,
        public_url: str,
    ) -> None:
        payload = {
            'paste_id': paste_id,
            'public_url': public_url,
        }
        await self.__produce(
            user_id=user_id,
            event='published',
            payload=payload,
        )