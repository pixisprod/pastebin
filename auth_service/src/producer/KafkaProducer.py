from aiokafka import AIOKafkaProducer

from src.config import Settings


config = Settings.load()


class KafkaProducer():
    def __init__(self):
        self.__producer: AIOKafkaProducer = AIOKafkaProducer(
            bootstrap_servers=config.kafka.server,
        )
    
    async def __start(self):
        await self.__producer.start()


    async def __stop(self):
        await self.__producer.stop()

    
    async def send(self, topic: str, value: bytes):
        await self.__start()
        try:
            await self.__producer.send(topic, value)
        finally:
            await self.__stop()


    @classmethod
    def load(cls):
        return cls()