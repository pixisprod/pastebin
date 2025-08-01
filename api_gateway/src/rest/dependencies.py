from typing import Annotated

from fastapi import Depends

from src.rest.HttpManager import HttpManager


async def get_http_manager():
    manager = HttpManager()
    try:
        yield manager
    finally:
        await manager.close()
    

http_manager_dep = Annotated[HttpManager, Depends(get_http_manager)]