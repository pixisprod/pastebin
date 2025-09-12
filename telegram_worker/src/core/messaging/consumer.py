import json

from aiogram import Bot
from aiokafka import AIOKafkaConsumer, ConsumerRecord

from lib.kafka.consumer import AioConsumer


class TelegramConsumer:
    def __init__(self, consumer: AIOKafkaConsumer, tg_bot: Bot):
        self.__low_level_consumer = consumer
        self.__consumer = AioConsumer(consumer=self.__low_level_consumer)
        self.__bot = tg_bot

        @self.__consumer.handler('sent')
        async def _(msg: ConsumerRecord):
            user = int(msg.key.decode())
            decoded = json.loads(msg.value)
            message = decoded['payload']['message']
            print(user)
            await self.__bot.send_message(chat_id=user, text=message)
            

    
    async def consume(self):
        await self.__consumer.consume()