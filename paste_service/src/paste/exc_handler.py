from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.paste import exceptions


def init_handlers(app: FastAPI):
    @app.exception_handler(exceptions.PasteNotFoundException)
    async def paste_not_found_handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status_code=status.HTTP_404_NOT_FOUND)
    
    @app.exception_handler(exceptions.PublicUrlAlreadyExistsException)
    async def public_url_already_exists_handler(request: Request, exc: Exception):
        return JSONResponse({'msg': str(exc)}, status_code=status.HTTP_409_CONFLICT)