from aiokafka import ConsumerRecord


async def handle_record(record: ConsumerRecord):
    match record.topic:
        case _: print('No logic for this topic')