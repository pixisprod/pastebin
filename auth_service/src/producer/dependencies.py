from typing import Annotated

from fastapi import Depends

from src.producer.KafkaProducer import KafkaProducer

async def get_producer():
    producer = KafkaProducer()
    return producer

kafka_producer_dep = Annotated[KafkaProducer, Depends(get_producer)]