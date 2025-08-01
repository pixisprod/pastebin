from typing import Annotated

from fastapi import Depends
from aiokafka import AIOKafkaProducer

from src.config import Settings

Config = Settings.load()


class KafkaProducerManager:
    def __init__(self) -> None:
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=Config.kafka.bootstrap_server
        )
    

    async def __open_conn(self) -> None:
        await self.__producer.start()


    async def __close_conn(self) -> None:
        await self.__producer.stop()


    async def send(self, topic: str, value: bytes) -> None:
        await self.__open_conn()
        try:
            await self.__producer.send(topic, value)
        finally:
            await self.__close_conn()

    @classmethod
    async def load(cls):
        return cls()


producer_dep = Annotated[
    KafkaProducerManager,
    Depends(KafkaProducerManager.load),
]