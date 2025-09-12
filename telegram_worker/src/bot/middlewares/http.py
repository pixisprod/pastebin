from aiogram import BaseMiddleware
from httpx import AsyncClient


class HttpMiddleware(BaseMiddleware):
    def __init__(self, client: AsyncClient):
        self.__client = client

    async def __call__(
        self, 
        handler, 
        event, 
        data: dict[str, any],
    ):
        data['http'] = self.__client
        return await handler(event, data)