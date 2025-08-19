from fastapi import Request

from src.paste.PasteService import PasteService


async def get_service_from_request(
    request: Request,
    service_key: str,
) -> PasteService:
    return getattr(request.state, service_key)


