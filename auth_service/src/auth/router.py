import datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from schemas_lib.auth_service.UserSchema import UserSchema
from schemas_lib.auth_service.UserRegisteredSchema import UserRegisteredSchema
from schemas_lib.auth_service.UserLogonSchema import UserLogonSchema
from schemas_lib.auth_service.topics import AuthTopics

from src.auth.dependencies import user_repository_dep, jwt_manager_dep
from src.database import db_dep
from src.config import Settings
from src.producer.dependencies import kafka_producer_dep


config = Settings.load()


router = APIRouter(
    tags=['Auth']
)


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(
    user: UserSchema, 
    user_rep: user_repository_dep, 
    db: db_dep,
    kafka_producer: kafka_producer_dep,
):
    new_user_id = await user_rep.create_user(user, db)
    await kafka_producer.send(
        topic=AuthTopics.NewUser,
        value=UserRegisteredSchema(user_id=new_user_id, email=user.email).model_dump_json().encode()
    )
    msg = {'msg': 'User successfully created'}
    return JSONResponse(msg)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    credentials: UserSchema, 
    user_rep: user_repository_dep, 
    db: db_dep,
    jwt_manager: jwt_manager_dep,
    kafka_producer: kafka_producer_dep,
) -> None:
    user = await user_rep.login_user(credentials, db)
    await kafka_producer.send(
        topic=AuthTopics.LoginUser,
        value=UserLogonSchema(user_id=user.id, email=user.email).model_dump_json().encode(),
    )
    access_token = jwt_manager.create_access_token(
        user_id=user.id,
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