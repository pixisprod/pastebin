from typing import Annotated

from fastapi import Depends

from src.paste.PasteRepository import PasteRepository


async def get_paste_repository():
    repository = PasteRepository()
    return repository

paste_repository_dep = Annotated[PasteRepository, Depends(get_paste_repository)]