from typing import Annotated

from fastapi import Depends

from src.auth.security.JwtManager import JwtManager
from src.config import Settings


config = Settings.load()


async def get_jwt_manager():
    manager = JwtManager(
        secret_key=config.jwt.secret_key.get_secret_value(),
        algorithm=config.jwt.algorithm,
        access_lifetime_sec=config.jwt.access_token_lifetime_seconds,
        refresh_lifetime_sec=config.jwt.refresh_token_lifetime_seconds,
    )
    return manager

jwt_manager_dep = Annotated[JwtManager, Depends(get_jwt_manager)]


