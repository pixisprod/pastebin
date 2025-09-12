from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.core.redis import get_redis_conn
from src.core.security import verify_token
from src.database.core import get_db
from src.core.service import NotificationService
from src.config import Settings


config = Settings.load()


def get_service(request: Request):
    service = getattr(request.state, config.app.service_state_key)
    return service


redis_dep = Annotated[Redis, Depends(get_redis_conn)]
user_dep = Annotated[dict, Depends(verify_token)]
db_dep = Annotated[AsyncSession, Depends(get_db)]
service_dep = Annotated[NotificationService, Depends(get_service)]
