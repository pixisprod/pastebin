from eventhub.kafka.producer.Producer import Producer
from eventhub.avro.SRAvroCodec import SRAvroCodec
from eventhub.confluent.ConfluentSRClient import ConfluentSRClient


class UserEventsPublisher:
    def __init__(
        self,
        kafka_producer: Producer,
        avro_codec: SRAvroCodec,
        sr_client: ConfluentSRClient,
    ):
        self.kafka_producer = kafka_producer
        self.avro_codec = avro_codec
        self.sr_client = sr_client


    async def publish_registered(
        self,
        user_id: int,
        user_email: str,
        topic: str,
    ) -> None:
        schema_id_key = await self.sr_client.get_schema_id_by_subject(
            subject=f'{topic}-key',
        )
        schema_id_val = await self.sr_client.get_schema_id_by_subject(
            subject=f'{topic}-value',
        )
        key = await self.avro_codec.serialize(
            schema_id=schema_id_key, 
            record={'id': user_id},
        )
        value = await self.avro_codec.serialize(
            schema_id=schema_id_val,
            record={'email': user_email}
        )
        await self.kafka_producer.send(topic, value, key)

