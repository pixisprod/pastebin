from fastapi import APIRouter, Path, status, Query
from fastapi.responses import JSONResponse

from schemas_lib.paste_service.PastePublishSchema import PastePublishSchema
from schemas_lib.paste_service.PasteEditSchema import PasteEditSchema

from src.paste.dependencies import paste_repository_dep
from src.paste.schemas import PasteOut
from src.database import db_dep


router = APIRouter(
    prefix='/pastes',
)


@router.patch('/{uid}/{pid}', response_model=PasteOut, status_code=status.HTTP_200_OK)
async def update_paste(
    paste_rep: paste_repository_dep,
    db: db_dep,
    new_paste_data: PasteEditSchema,
    uid: int = Path(gt=0),
    pid: int = Path(gt=0)
):
    updated_paste = await paste_rep.update_paste(
        new_paste_data=new_paste_data,
        paste_id=pid,
        user_id=uid,
        db=db,
    )
    return updated_paste


@router.get('/public/{public_paste_url}', response_model=PasteOut, status_code=status.HTTP_200_OK)
async def get_public_paste(
    paste_rep: paste_repository_dep, 
    db: db_dep,
    public_paste_url: str = Path(min_length=1, max_length=36),
):
    paste = await paste_rep.get_public_paste(public_paste_url, db)
    return paste

@router.get('/{uid}', response_model=list[PasteOut], status_code=status.HTTP_200_OK)
async def get_pastes(
    paste_rep: paste_repository_dep, 
    db: db_dep,
    uid: int = Path(gt=0),
):
    orm_pastes = await paste_rep.get_pastes(uid, db)
    return orm_pastes


@router.get('/{uid}/{pid}', status_code=status.HTTP_200_OK, response_model=PasteOut)
async def get_paste(
    paste_rep: paste_repository_dep,
    db: db_dep,
    uid: int = Path(gt=0),
    pid: int = Path(gt=0),
):
    paste = await paste_rep.get_paste(uid, pid, db)
    return paste


@router.post('/{uid}/{pid}/publish', status_code=status.HTTP_200_OK)
async def publish_paste(
    content: PastePublishSchema,
    paste_rep: paste_repository_dep,
    db: db_dep,
    uid: int = Path(gt=0),
    pid: int = Path(gt=0),
):
    public_url = await paste_rep.publish_paste(uid, pid, db, content.public_url)
    msg = {'msg': 'Paste published', 'public_url': public_url}
    return JSONResponse(msg)


@router.delete('/{uid}/{pid}', status_code=status.HTTP_200_OK)
async def delete_paste(
    paste_rep: paste_repository_dep,
    db: db_dep,
    uid: int = Path(gt=0), 
    pid: int = Path(gt=0),
):
    deleted_paste_id = await paste_rep.delete_paste(db, uid, pid)
    msg = {'msg': 'Paste deleted', 'deleted_paste_id': deleted_paste_id}
    return JSONResponse(msg)