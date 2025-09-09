from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def get_start_keyboard(is_telegram_linked: bool) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = ['About us', 'Our website']
    builder.adjust(2)
    if not is_telegram_linked:
        builder.button('Link telegram to PasteBin')
        builder.adjust(1, 2)
    for button in buttons:
        builder.button(text=button)
    return builder.as_markup()
    