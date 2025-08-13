from pathlib import Path
import json
import asyncio
from httpx import ConnectError
from contextlib import asynccontextmanager

import aiofiles
from eventhub.confluent.ConfluentSRClient import ConfluentSRClient


SCHEMA_DIR = Path(__file__).parent.parent / 'schemas'


@asynccontextmanager
async def confluent_sr_context(server: str):
    try:
        client = ConfluentSRClient(server)
        yield client
    finally:
        await client.close()


async def main():
    async with confluent_sr_context('http://schema-registry:8081') as sr_client:
        for path in SCHEMA_DIR.rglob('*.avsc'):
            event_type = path.parent.name
            key_type = path.stem
            schema_subject = f'{event_type}-{key_type}'
            schema: dict
            async with aiofiles.open(path, 'r') as file:
                schema = json.loads(await file.read())
            while True:
                try:
                    await sr_client.register_schema(schema_subject, schema)
                    break
                except ConnectError:
                    print('Connection failed, retrying in 5 seconds..')
                    await asyncio.sleep(5)

    print('Schemas successfully loaded!')

if __name__ == '__main__':
    asyncio.run(main())
