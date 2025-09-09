from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from src.config import Settings
from src.bot.keyboards import get_start_keyboard


config = Settings.load()


bot = Bot(
    token=config.telegram.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        text=f'Hello **{message.from_user.full_name}** from PasteBin',
        reply_markup=get_start_keyboard(False),
    )