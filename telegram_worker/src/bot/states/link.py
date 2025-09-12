from aiogram.fsm.state import StatesGroup, State


class LinkTelegram(StatesGroup):
    code = State()