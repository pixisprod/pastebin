from fastapi import APIRouter, Path, status
from fastapi.responses import JSONResponse

from src.core.schemas import (
    PasteSchema, PastePublishSchema, PasteEditSchema
)
from src.core.schemas import PasteOut
from src.core.dependencies import service_dep
from src.database.dependencies import db_dep
from src.core.security.dependencies import user_dep
from src.core.utils import get_user_id_from_payload
from src.config import Settings


config = Settings.load()


router = APIRouter(
    tags=['Paste 🗒️']
)


@router.get('/public/{public_paste_url}', response_model=PasteOut, status_code=status.HTTP_200_OK)
async def get_public_paste(
    db: db_dep,
    paste_service: service_dep,
    public_paste_url: str = Path(min_length=1, max_length=36),
):
    paste = await paste_service.get_public_paste(db, public_paste_url)
    return paste


@router.get('/', response_model=list[PasteOut], status_code=status.HTTP_200_OK)
async def get_pastes( 
    user: user_dep,
    db: db_dep,
    service: service_dep,
):
    user_id = get_user_id_from_payload(user)
    orm_pastes = await service.get_pastes(db, user_id)
    return orm_pastes


@router.get('/{paste_id}', status_code=status.HTTP_200_OK, response_model=PasteOut)
async def get_paste(
    db: db_dep,
    service: service_dep,
    user: user_dep,
    paste_id: int = Path(gt=0),
):
    user_id = get_user_id_from_payload(user)
    paste = await service.get_paste(db, user_id, paste_id)
    return paste


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_paste(
    db: db_dep,
    service: service_dep,
    paste: PasteSchema,
    user: user_dep, 
):
    user_id = get_user_id_from_payload(user)
    new_paste_id = await service.add_paste(db, user_id, paste)
    msg = {'msg': 'Paste successfully added!', 'new_paste_id': new_paste_id}
    response = JSONResponse(msg)
    return response


@router.post('/{paste_id}/publish', status_code=status.HTTP_200_OK)
async def publish_paste(
    body: PastePublishSchema,
    service: service_dep,
    db: db_dep,
    user: user_dep,
    paste_id: int = Path(gt=0),
):
    user_id = get_user_id_from_payload(user)
    public_url = await service.publish_paste(
        user_id=user_id,
        paste_id=paste_id,
        db=db,
        public_url=body.public_url,
    )
    msg = {'msg': 'Paste published', 'public_url': public_url}
    return JSONResponse(msg)


@router.delete('/{paste_id}', status_code=status.HTTP_200_OK)
async def delete_paste(
    db: db_dep,
    service: service_dep,
    user: user_dep, 
    paste_id: int = Path(gt=0),
):
    user_id = get_user_id_from_payload(user)
    deleted_paste_id = await service.delete_paste(user_id, paste_id, db)
    msg = {'msg': 'Paste deleted', 'paste_id': deleted_paste_id}
    return JSONResponse(msg)


@router.patch('/{paste_id}', response_model=PasteOut, status_code=status.HTTP_200_OK)
async def update_paste(
    db: db_dep,
    new_paste_data: PasteEditSchema,
    service: service_dep,
    user: user_dep,
    paste_id: int = Path(gt=0)
):
    user_id = get_user_id_from_payload(user)
    updated_paste = await service.edit_paste(
        user_id=user_id,
        paste_id=paste_id,
        db=db,
        upd_paste_data=new_paste_data,
    )
    return updated_paste
