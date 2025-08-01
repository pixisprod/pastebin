from fastapi import APIRouter, status, Path
from fastapi.responses import JSONResponse

from schemas_lib.paste_service.PasteSchema import PasteEntrySchema, PasteSchema
from schemas_lib.paste_service.topics import PasteTopics
from schemas_lib.paste_service.PastePublishSchema import PastePublishSchema
from schemas_lib.paste_service.PasteEditSchema import PasteEditSchema

from src.rest.dependencies import http_manager_dep
from src.auth.jwt.dependencies import user_dep
from src.KafkaProducerManager import producer_dep
from src.config import Settings


router = APIRouter(prefix='/pastes', tags=['Pastes 💬'])
config = Settings.load()


@router.get('/', summary='Get all your pastes')
async def get_pastes(uid: user_dep, http_manager: http_manager_dep):
    r = await http_manager.get(f'{config.paste_service.url}/{config.paste_service.api_ver}/pastes/{uid}')
    response = JSONResponse(r.json(), r.status_code)
    return response


@router.get('/public/{public_url}', tags=['Public 👤'], summary='Get public paste by url')
async def get_public_paste(
    http_manager: http_manager_dep,
    public_url: str = Path(min_length=1)
):
    r = await http_manager.get(
        f'{config.paste_service.url}/{config.paste_service.api_ver}/pastes/public/{public_url}',
    )
    response = JSONResponse(r.json(), r.status_code)
    return response


@router.get('/{pid}', summary='Get your paste by id')
async def get_paste(
    uid: user_dep,
    http_manager: http_manager_dep,
    pid: int = Path(gt=0),
):
    r = await http_manager.get(
        f'{config.paste_service.url}/{config.paste_service.api_ver}/pastes/{uid}/{pid}'
    )
    response = JSONResponse(r.json(), r.status_code)
    return response


@router.post('/', status_code=status.HTTP_201_CREATED, summary='Add new paste')
async def add_paste(paste: PasteSchema, uid: user_dep, producer: producer_dep):
    entry = PasteEntrySchema(user_id=uid, paste=paste)
    message = entry.model_dump_json().encode()
    await producer.send(PasteTopics.AddPaste, message)
    msg = {'msg': 'Paste received'}
    return JSONResponse(msg)


@router.post('/{pid}/publish', summary='Publish your paste')
async def publish_paste(
    body: PastePublishSchema, 
    uid: user_dep,
    http_manager: http_manager_dep,
    pid: int = Path(gt=0),
):
    r = await http_manager.post(
        f'{config.paste_service.url}/{config.paste_service.api_ver}/pastes/{uid}/{pid}/publish',
        body.model_dump()
    )
    response = JSONResponse(r.json(), r.status_code)
    return response


@router.delete('/{pid}', summary='Delete your paste by id')
async def delete_paste(
    uid: user_dep,
    http_manager: http_manager_dep,
    pid: int = Path(gt=0),
):
    r = await http_manager.delete(
        f'{config.paste_service.url}/{config.paste_service.api_ver}/pastes/{uid}/{pid}'
    )
    return JSONResponse(r.json(), r.status_code)


@router.patch('/{pid}', summary='Edit your paste by id')
async def update_paste(
    http_manager: http_manager_dep,
    new_paste_data: PasteEditSchema,
    uid: user_dep,
    pid: int = Path(gt=0),
):
    r = await http_manager.patch(
        f'{config.paste_service.url}/{config.paste_service.api_ver}/pastes/{uid}/{pid}',
        new_paste_data.model_dump(),
    )
    response = JSONResponse(r.json(), r.status_code)
    return response