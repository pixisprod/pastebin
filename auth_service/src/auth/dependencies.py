from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from src.auth.AuthService import AuthService
from src.database.UserDAO import UserDAO
from src.auth.security.JwtManager import JwtManager
from src.auth.security.bcrypt import get_bcrypt_hasher


async def get_auth_service():
    repository = AuthService(UserDAO())
    return repository

auth_service_dep = Annotated[AuthService, Depends(get_auth_service)]


async def get_jwt_manager():
    manager = JwtManager()
    return manager

jwt_manager_dep = Annotated[JwtManager, Depends(get_jwt_manager)]


bcrypt_hasher_dep = Annotated[CryptContext, Depends(get_bcrypt_hasher)]