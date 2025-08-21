import jose
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from eventhub.auth.jwt import exceptions as token_exceptions

from src.paste import exceptions as paste_exceptions


def register_handler(app: FastAPI, exc_type: type[Exception], status_code: int):
    @app.exception_handler(exc_type)
    async def handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status_code=status_code)
    

def init_handlers(app: FastAPI):
    exceptions_mapping: dict[type[Exception], int] = {
        paste_exceptions.PasteNotFoundException: status.HTTP_404_NOT_FOUND,
        paste_exceptions.PublicUrlAlreadyExistsException: status.HTTP_409_CONFLICT,
        token_exceptions.TokenMissingException: status.HTTP_401_UNAUTHORIZED,
        jose.exceptions.JWTError: status.HTTP_401_UNAUTHORIZED,
    }

    for exc, code in exceptions_mapping.items():
        register_handler(app, exc, code)
    