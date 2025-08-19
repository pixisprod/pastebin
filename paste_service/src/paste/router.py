from fastapi import APIRouter, Path, status, Request
from fastapi.responses import JSONResponse

from eventhub.pydantic.paste_service.PasteSchema import PasteSchema

from src.paste.schemas import PasteOut
from src.database.dependencies import db_dep
from src.paste.utils import get_service_from_request

from src.config import Settings


config = Settings.load()


router = APIRouter(
    prefix='/pastes',
)


# @router.get('/public/{public_paste_url}', response_model=PasteOut, status_code=status.HTTP_200_OK)
# async def get_public_paste(
#     paste_rep: paste_repository_dep, 
#     db: db_dep,
#     public_paste_url: str = Path(min_length=1, max_length=36),
# ):
#     paste = await paste_rep.get_public_paste(public_paste_url, db)
#     return paste


@router.get('/{user_id}', response_model=list[PasteOut], status_code=status.HTTP_200_OK)
async def get_pastes( 
    db: db_dep,
    request: Request,
    user_id: int = Path(gt=0),
):
    service = await get_service_from_request(
        request=request,
        service_key=config.app.service_state_key,
    )
    orm_pastes = await service.get_pastes(db, user_id)
    return orm_pastes


@router.get('/{user_id}/{paste_id}', status_code=status.HTTP_200_OK, response_model=PasteOut)
async def get_paste(
    db: db_dep,
    request: Request,
    user_id: int = Path(gt=0),
    paste_id: int = Path(gt=0),
):
    service = await get_service_from_request(request, config.app.service_state_key)
    paste = await service.get_paste(db, user_id, paste_id)
    return paste


@router.post('/{user_id}', status_code=status.HTTP_201_CREATED)
async def add_paste(
    db: db_dep,
    request: Request,
    paste: PasteSchema,
    user_id: int = Path(gt=0), 
):
    service = await get_service_from_request(request, config.app.service_state_key)
    new_paste_id = await service.add_paste(db, user_id, paste)
    msg = {'msg': 'Paste successfully added!', 'new_paste_id': new_paste_id}
    response = JSONResponse(msg)
    return response


# @router.post('/{uid}/{pid}/publish', status_code=status.HTTP_200_OK)
# async def publish_paste(
#     content: PastePublishSchema,
#     paste_rep: paste_repository_dep,
#     db: db_dep,
#     uid: int = Path(gt=0),
#     pid: int = Path(gt=0),
# ):
#     public_url = await paste_rep.publish_paste(uid, pid, db, content.public_url)
#     msg = {'msg': 'Paste published', 'public_url': public_url}
#     return JSONResponse(msg)


@router.delete('/{user_id}/{paste_id}', status_code=status.HTTP_200_OK)
async def delete_paste(
    db: db_dep,
    request: Request,
    user_id: int = Path(gt=0), 
    paste_id: int = Path(gt=0),
):
    service = await get_service_from_request(request, config.app.service_state_key)
    deleted_paste_id = await service.delete_paste(user_id, paste_id, db)
    msg = {'msg': 'Paste deleted', 'paste_id': deleted_paste_id}
    return JSONResponse(msg)


# @router.patch('/{uid}/{pid}', response_model=PasteOut, status_code=status.HTTP_200_OK)
# async def update_paste(
#     paste_rep: paste_repository_dep,
#     db: db_dep,
#     new_paste_data: PasteEditSchema,
#     uid: int = Path(gt=0),
#     pid: int = Path(gt=0)
# ):
#     updated_paste = await paste_rep.update_paste(
#         new_paste_data=new_paste_data,
#         paste_id=pid,
#         user_id=uid,
#         db=db,
#     )
#     return updated_paste
