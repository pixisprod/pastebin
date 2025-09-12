from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse

from lib.schemas.pydantic import LinkTelegramSchema

from src.core.dependencies import (
    user_dep, redis_dep, service_dep, db_dep
)


router = APIRouter()


@router.get('/telegram-link-code-generate', status_code=status.HTTP_201_CREATED)
async def _(
    user: user_dep, 
    service: service_dep,
    redis: redis_dep,
):
    code = await service.telegram_set_code(redis=redis, user_id=user.get('sub'))
    msg = {'msg': 'Code successfully generated', 'code': code}
    response = JSONResponse(msg)
    return response


@router.post('/telegram-link-code-check', status_code=status.HTTP_200_OK)
async def _(
    service: service_dep, 
    redis: redis_dep, 
    data: LinkTelegramSchema,
    db: db_dep,
):
    await service.telegram_confirm_code(
        db=db, 
        redis=redis, 
        code=data.code,
        telegram_uid=data.telegram_uid,
    )
    msg = {'msg': 'Successfully linked telegram', 'success': True}
    response = JSONResponse(msg)
    return response


@router.get('/is-telegram-linked', status_code=status.HTTP_200_OK)
async def _(db: db_dep, service: service_dep, telegram_id: int = Query(gt=0)):
    is_linked = await service.is_telegram_linked(db, telegram_id)
    msg = {'msg': 'Successful response', 'is_linked': is_linked}
    return JSONResponse(msg)
    