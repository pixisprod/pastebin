from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.auth import exceptions


def init_handlers(app: FastAPI):
    @app.exception_handler(exceptions.UserAlreadyExistsException)
    async def user_already_exists_handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status.HTTP_409_CONFLICT)
    
    @app.exception_handler(exceptions.UserIncorrectCredentialsException)
    async def user_incorrect_credentials_handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status.HTTP_401_UNAUTHORIZED)