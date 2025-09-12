from redis import asyncio as redis

from src.config import Settings


config = Settings.load()

redis_pool = redis.ConnectionPool.from_url(
    url='redis://redis',
    decode_responses=True,
)


def get_redis_conn() -> redis.Redis:
    return redis.Redis.from_pool(redis_pool)