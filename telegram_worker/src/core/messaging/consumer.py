import json

from aiokafka import AIOKafkaConsumer, ConsumerRecord

from lib.kafka.consumer import AioConsumer


class TelegramConsumer:
    def __init__(self, consumer: AIOKafkaConsumer):
        self.__low_level_consumer = consumer
        self.__consumer = AioConsumer(consumer=self.__low_level_consumer)

        @self.__consumer.handler('sent')
        async def _(msg: ConsumerRecord):
            decoded = json.loads(msg.value)
            message = decoded['payload']['message']
            print(message)
            

    
    async def consume(self):
        await self.__consumer.consume()