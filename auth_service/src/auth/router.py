import datetime

from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse

from eventhub.pydantic.auth_service.UserSchema import UserSchema

from src.auth.dependencies import (
    service_infra_dep, jwt_manager_dep
)
from src.database.core import db_dep
from src.config import Settings
from src.auth.AuthService import AuthService


config = Settings.load()


router = APIRouter(
    tags=['Auth']
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user: UserSchema, 
    db: db_dep,
    request: Request,
    infra: service_infra_dep,
):
    service: AuthService = getattr(request.state, config.app.service_state_key)
    new_user_id = await service.register_user(db, infra, user)
    msg = {'msg': 'User successfully created!', 'user_id': new_user_id}
    response = JSONResponse(msg)
    return response


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    credentials: UserSchema, 
    infra: service_infra_dep,
    db: db_dep,
    jwt_manager: jwt_manager_dep,
    request: Request,
) -> None:
    service: AuthService = request.state[config.app.service_state_key]
    user = await service.login_user(credentials, db, infra)
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