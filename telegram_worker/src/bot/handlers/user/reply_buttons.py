from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from redis import asyncio as aredis
from httpx import AsyncClient

from lib.schemas.pydantic import LinkTelegramSchema

from src.bot.keyboards.buttons import Buttons
from src.bot.states import LinkTelegram


router = Router(name='Buttons router')


@router.message(F.text==Buttons.Start.Links)
async def _(message: Message):
    text = (
        "*Useful Links*\n"
        "• ✨ [Author](https://github.com/pixisprod)\n"
        "• 📖 [Documentation](https://github.com/pixisprod/pastebin)\n"
    )
    await message.answer(text)


@router.message(F.text==Buttons.Start.AboutUs)
async def _(message: Message):
    text = (
        '*PasteBin*\n'
        '• ⛩️ This is a **learning project** built with FastAPI, Kafka, and a microservice architecture\n'
        '• 📦 This telegram bot is needed for notifications and further integration\n'
        '• 🧑‍💻 It’s created for practice and educational purposes only\n'
    )
    await message.answer(text)


@router.message(F.text==Buttons.Start.LinkTelegram)
async def _(message: Message, state: FSMContext):
    await message.answer('Enter the code received on the website')
    await state.set_state(LinkTelegram.code)

@router.message(LinkTelegram.code, F.text)
async def _(message: Message, state: FSMContext, redis: aredis.Redis, http: AsyncClient):
    code = message.text
    if not await redis.exists(f'tg_code:{code}'):
        await message.answer('Incorrect code!')
        return
    body = LinkTelegramSchema(
        code=code,
        telegram_uid=message.from_user.id,
    )
    url = 'http://notification_service:8000/telegram-link-code-check'
    r = await http.post(url, json=body.model_dump())
    if r.status_code == 200:
        await message.answer('Code correct, account connected!')
        await state.clear()
        return
    await message.answer('Code server refused code')
    
        
    
@router.message(LinkTelegram.code)
async def _(message: Message, state: FSMContext):
    await message.answer('Code must be STRING!')
    

    