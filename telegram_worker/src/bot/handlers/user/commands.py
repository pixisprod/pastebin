from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from httpx import AsyncClient
from redis import asyncio as aredis

from src.bot.keyboards import get_start_keyboard


router = Router(name='Commands Router')


@router.message(CommandStart())
async def start(message: Message, http: AsyncClient, redis: aredis.Redis):
    url = f'http://notification_service:8000/is-telegram-linked?telegram_id={message.from_user.id}'
    r = await http.get(url)
    r.raise_for_status()
    data = r.json()
    is_linked = data['is_linked']
    await message.answer(
        text=f'Hello {message.from_user.full_name} modules!',
        reply_markup=get_start_keyboard(is_linked),
    )


