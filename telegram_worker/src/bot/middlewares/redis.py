from aiogram import BaseMiddleware
from redis import asyncio as redis


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis: redis.Redis):
        self.__redis = redis

    async def __call__(
        self, 
        handler, 
        event, 
        data: dict[str, any],
    ):
        data['redis'] = self.__redis
        return await handler(event, data)