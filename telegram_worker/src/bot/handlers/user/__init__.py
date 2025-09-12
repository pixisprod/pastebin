from aiogram import Router

from .commands import router as commands_router
from .reply_buttons import router as reply_buttons_router


user_router = Router(name='UserRouter')
user_router.include_router(commands_router)
user_router.include_router(reply_buttons_router)