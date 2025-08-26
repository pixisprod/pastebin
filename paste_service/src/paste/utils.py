def get_user_id_from_payload(payload: dict) -> int:
    return int(payload.get('sub'))
