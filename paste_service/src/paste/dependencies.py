from typing import Annotated

from fastapi import Depends, Request

from src.paste.service import PasteService
from src.config import Settings


config = Settings.load()


def get_service(request: Request):
    service = getattr(request.state, config.app.service_state_key)
    return service

service_dep = Annotated[PasteService, Depends(get_service)]