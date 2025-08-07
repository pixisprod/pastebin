import datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from eventhub.pydantic.auth_service.UserSchema import UserSchema

from src.auth.dependencies import (
    auth_service_dep, jwt_manager_dep, bcrypt_hasher_dep,
)
from src.database.core import db_dep
from src.config import Settings


config = Settings.load()


router = APIRouter(
    tags=['Auth']
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user: UserSchema, 
    service: auth_service_dep,
    db: db_dep,
    hasher: bcrypt_hasher_dep,
):
    new_user_id = await service.register_user(db, user, hasher)
    msg = {'msg': 'User successfully created!', 'user_id': new_user_id}
    response = JSONResponse(msg)
    return response


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    credentials: UserSchema, 
    service: auth_service_dep,
    db: db_dep,
    jwt_manager: jwt_manager_dep,
    hasher: bcrypt_hasher_dep
) -> None:
    user = await service.login_user(credentials, db, hasher)
    access_token = jwt_manager.create_access_token(
        user_id = user.id,
        now=datetime.datetime.now(datetime.UTC),
    )
    refresh_token = jwt_manager.create_refresh_token(
        user_id=user.id,
        now=datetime.datetime.now(datetime.UTC),
    )
    msg = {'msg': 'Successful login'}
    response = JSONResponse(msg)
    response.set_cookie(config.jwt.access_token_cookie_name, access_token)
    response.set_cookie(config.jwt.refresh_token_cookie_name, refresh_token)
    return response