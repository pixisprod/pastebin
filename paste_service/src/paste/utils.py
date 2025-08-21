from fastapi import Request

from src.paste.service import PasteService


def get_user_id_from_payload(payload: dict) -> int:
    return int(payload.get('sub'))


