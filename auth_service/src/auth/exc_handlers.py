from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from lib.auth.jwt import exceptions as jwtexc

from src.auth import exceptions


def register_handler(app: FastAPI, exc_type: type[Exception], status_code: int):
    @app.exception_handler(exc_type)
    async def handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status_code=status_code)


def init_handlers(app: FastAPI):
    exceptions_mapping: dict[type[Exception], int] = {
        exceptions.UserAlreadyExistsException: status.HTTP_409_CONFLICT,
        exceptions.UserIncorrectCredentialsException: status.HTTP_401_UNAUTHORIZED,
        exceptions.UserNotFoundException: status.HTTP_404_NOT_FOUND,
        jwtexc.TokenMissingException: status.HTTP_401_UNAUTHORIZED
    }

    for exc, code in exceptions_mapping.items():
        register_handler(app, exc, code)