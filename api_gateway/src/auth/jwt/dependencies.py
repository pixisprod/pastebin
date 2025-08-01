from typing import Annotated

from fastapi import Depends, Cookie

from src.auth.jwt.JwtValidator import JwtValidator
from src.auth.jwt import exceptions

def verify_token(token: str = Cookie(None, alias='access_token')):
    if not token:
        raise exceptions.NoJwtTokenException()
    validator = JwtValidator.load()
    return validator.decode_token(token)

user_dep = Annotated[int, Depends(verify_token)]

def get_jwt_validator():
    validator = JwtValidator.load()
    return validator

jwt_validator_dep = Annotated[JwtValidator, Depends(get_jwt_validator)]

