from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from src.config import Settings


config = Settings.load()


def verify_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    return jwt.decode(
        token=token.credentials, 
        key=config.jwt.secret_key.get_secret_value(),
        algorithms=config.jwt.algorithm,
    )
