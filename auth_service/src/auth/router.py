import datetime

from fastapi import APIRouter, status, Request, Cookie
from fastapi.responses import JSONResponse

from eventhub.pydantic.auth_service.UserSchema import UserSchema

from src.auth.dependencies import jwt_manager_dep
from src.database.core import db_dep
from src.config import Settings
from src.auth.AuthService import AuthService
from src.utils import get_service_from_request
from src.auth import exceptions


config = Settings.load()


router = APIRouter(
    tags=['Auth']
)


@router.post('/refresh-access-token', status_code=status.HTTP_200_OK)
async def refresh_access_token(
    request: Request,
    jwt_manager: jwt_manager_dep,
    db: db_dep,
    token=Cookie(default=None, alias=config.jwt.access_token_cookie_name),
):
    if not token:
        raise exceptions.RefreshTokenNotFoundException()
    service: AuthService = await get_service_from_request(
        request=request,
        service_key=config.app.service_state_key,
    )
    now = datetime.datetime.now(datetime.UTC)
    new_access_token = await service.refresh_token(
        token=token,
        now=now,
        db=db,
        jwt_manager=jwt_manager,
    )
    msg = {'msg': 'Access token successfully refreshed'}
    response = JSONResponse(msg)
    response.set_cookie(config.jwt.access_token_cookie_name, new_access_token)
    return response


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user: UserSchema, 
    db: db_dep,
    request: Request,
):
    service: AuthService = await get_service_from_request(
        request=request,
        service_key=config.app.service_state_key,
    )
    new_user_id = await service.register_user(db, user)
    msg = {'msg': 'User successfully created!', 'user_id': new_user_id}
    response = JSONResponse(msg)
    return response


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    credentials: UserSchema, 
    db: db_dep,
    jwt_manager: jwt_manager_dep,
    request: Request,
) -> None:
    service: AuthService = await get_service_from_request(
        request=request,
        service_key=config.app.service_state_key,
    )
    user = await service.login_user(credentials, db)
    now = datetime.datetime.now(datetime.UTC)
    access_token = jwt_manager.create_access_token(
        user_id = user.id,
        now=now,
    )
    refresh_token = jwt_manager.create_refresh_token(
        user_id=user.id,
        now=now,
    )
    msg = {'msg': 'Successful login'}
    response = JSONResponse(msg)
    response.set_cookie(config.jwt.access_token_cookie_name, access_token)
    response.set_cookie(config.jwt.refresh_token_cookie_name, refresh_token)
    return response