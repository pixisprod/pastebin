from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse

from src.auth.jwt import exceptions as jwt_exceptions
from jose import exceptions as jose_exceptions


def init_handlers(app: FastAPI):
    @app.exception_handler(jwt_exceptions.NoJwtTokenException)
    async def no_jwt_token_handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status.HTTP_401_UNAUTHORIZED)
    
    
    @app.exception_handler(jose_exceptions.JWTError)
    async def jwt_error_exception(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status.HTTP_401_UNAUTHORIZED)