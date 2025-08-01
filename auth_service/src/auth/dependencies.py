from typing import Annotated

from fastapi import Depends

from src.auth.UserRepository import UserRepository
from src.auth.security.JwtManager import JwtManager


async def get_user_repository():
    repository = UserRepository()
    return repository

user_repository_dep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_jwt_manager():
    manager = JwtManager()
    return manager

jwt_manager_dep = Annotated[JwtManager, Depends(get_jwt_manager)]