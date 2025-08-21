import datetime

from fastapi import APIRouter, status, Cookie
from fastapi.responses import JSONResponse

from eventhub.auth.jwt import exceptions

from src.auth.schemas import UserSchema
from src.auth.dependencies import jwt_manager_dep, service_dep
from src.config import Settings
from src.database.core import db_dep


config = Settings.load()


router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/refresh-access-token', status_code=status.HTTP_200_OK)
async def refresh_access_token(
    service: service_dep,
    jwt_manager: jwt_manager_dep,
    db: db_dep,
    token=Cookie(default=None, alias=config.jwt.refresh_token_cookie_name),
):
    if not token:
        raise exceptions.RefreshTokenMissingException()
    now = datetime.datetime.now(datetime.UTC)
    new_access_token = await service.refresh_token(
        token=token,
        now=now,
        db=db,
        jwt_manager=jwt_manager,
    )
    msg = {
        'msg': 'Access token successfully refreshed',
        'access_token': new_access_token
    }
    response = JSONResponse(msg)
    return response


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user: UserSchema, 
    db: db_dep,
    service: service_dep,
):
    new_user_id = await service.register_user(db, user)
    msg = {'msg': 'User successfully created!', 'user_id': new_user_id}
    response = JSONResponse(msg)
    return response


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    credentials: UserSchema, 
    db: db_dep,
    jwt_manager: jwt_manager_dep,
    service: service_dep,
) -> None:
    user = await service.login_user(credentials, db)
    now = datetime.datetime.now(datetime.UTC)
    access_token = jwt_manager.create_access_token(
        user_id=user.id,
        now=now,
    )
    refresh_token = jwt_manager.create_refresh_token(
        user_id=user.id,
        now=now,
    )
    msg = {
        'msg': 'Successful login',
        'access_token': access_token
    }
    response = JSONResponse(msg)
    response.set_cookie(config.jwt.refresh_token_cookie_name, refresh_token)
    return response