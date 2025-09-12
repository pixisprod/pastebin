from redis import asyncio as redis


redis_conn = redis.from_url('redis://redis')
