import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import Settings
from src.core.utils import setup_consumer, ngrok_manager
from src.bot.core import bot
from src.core import api_router
from src.core.http import client


config = Settings.load()
kafka_server = f'{config.kafka.server}:{config.kafka.server_port}'


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with ngrok_manager('http://ngrok:4040') as ngrok:
        ngrok_tunnel_url = await ngrok.create_tunnel(
            address='telegram_worker:8000',
            protocol='http',
            name='telegram_bot',
        )
    webhook_url = f'{ngrok_tunnel_url}{config.telegram.bot_webhook}'
    await bot.set_webhook(webhook_url, drop_pending_updates=True)
    loop = asyncio.get_event_loop()
    consumer = setup_consumer(kafka_server)
    loop.create_task(consumer.consume())
    try:
        yield
    finally:
        await bot.session.close()
        await client.aclose()


app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)