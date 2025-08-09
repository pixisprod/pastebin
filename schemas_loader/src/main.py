from pathlib import Path
import json
import asyncio

import aiofiles

from eventhub.confluent.ConfluentSRClient import ConfluentSRClient


SCHEMA_DIR = Path(__file__).parent.parent / 'schemas'


async def main():
    confluent_client = ConfluentSRClient('http://schema-registry:8081')
    async with confluent_client as sr_client:
        for path in SCHEMA_DIR.rglob('*.avsc'):
            event_type = path.parent.name
            key_type = path.stem
            schema_subject = f'{event_type}-{key_type}'
            schema: dict
            async with aiofiles.open(path, 'r') as file:
                schema = json.loads(await file.read())
            await sr_client.register_schema(schema_subject, schema)

if __name__ == '__main__':
    asyncio.run(main())
