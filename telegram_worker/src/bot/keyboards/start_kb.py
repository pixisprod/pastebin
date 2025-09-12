from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from src.bot.keyboards.buttons import Buttons


def get_start_keyboard(is_telegram_linked: bool) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [Buttons.Start.AboutUs, Buttons.Start.Links]
    if not is_telegram_linked:
        builder.button(text=Buttons.Start.LinkTelegram)
    for button in buttons:
        builder.button(text=button)
    if not is_telegram_linked:
        builder.adjust(1, 2)
    else:
        builder.adjust(2)
    return builder.as_markup()
    