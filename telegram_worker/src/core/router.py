from fastapi import APIRouter, Request
from aiogram.types import Update

from src.config import Settings
from src.bot.core import dp, bot
from src.core import router


config = Settings.load()
router = APIRouter()


@router.post(config.telegram.bot_webhook)
async def process_update(request: Request) -> None:
    update = Update.model_validate(await request.json())
    await dp.feed_update(bot, update)
