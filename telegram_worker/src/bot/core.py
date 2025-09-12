from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import Settings
from src.bot.handlers import router
from src.bot.middlewares import RedisMiddleware, HttpMiddleware
from src.core.redis import redis_conn
from src.core.http import client


config = Settings.load()


bot = Bot(
    token=config.telegram.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()
dp.include_router(router)
dp.update.middleware(RedisMiddleware(redis_conn))
dp.update.middleware(HttpMiddleware(client))
