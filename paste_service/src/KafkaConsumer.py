import asyncio
import json

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from aiokafka.errors import KafkaConnectionError

from schemas_lib.paste_service.topics import PasteTopics
from schemas_lib.paste_service.PasteSchema import PasteEntrySchema

from src.config import Settings
from src.paste.PasteRepository import PasteRepository
from src.database import session_factory


config = Settings.load()

class KafkaConsumer:
    def __init__(self) -> None:
        self.__paste_rep: PasteRepository = PasteRepository()
        self.__consumer: AIOKafkaConsumer = AIOKafkaConsumer(
            *PasteTopics,
            bootstrap_servers=config.kafka.server,
            group_id='paste_service'
        )


    async def __consume(
        self, 
        msg: ConsumerRecord,
    ) -> None:
        match msg.topic:
            case PasteTopics.AddPaste:
                async with session_factory() as db:
                    data = PasteEntrySchema(**json.loads(msg.value))
                    await self.__paste_rep.add_paste(data.user_id, data.paste, db)



    async def start_consuming(self) -> None:
        while True:
            try:
                await self.__consumer.start()
                break
            except KafkaConnectionError:
                await asyncio.sleep(5) 
        try:
            async for msg in self.__consumer:
                await self.__consume(msg)
        finally:
            await self.__consumer.stop()

    @classmethod
    def load(cls):
        return cls()