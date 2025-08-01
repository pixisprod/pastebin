from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from schemas_lib.auth_service.UserSchema import UserSchema

from src.rest.dependencies import http_manager_dep
from src.config import Settings


router = APIRouter(
    prefix='/auth',
    tags=['Auth 🔒', 'Public 👤'],
)
config = Settings.load()


@router.post(
    path='/register-user', 
    status_code=status.HTTP_201_CREATED,
    summary='Register new user')
async def register_user(user: UserSchema, http_manager: http_manager_dep):
    r = await http_manager.post(
        f'{config.auth_service.url}/{config.auth_service.api_ver}/register', 
        user.model_dump()
    )
    return JSONResponse(r.json(), r.status_code)


@router.post(
    path='/login-user', 
    status_code=status.HTTP_200_OK,
    summary='Log in'
)
async def login_user(user: UserSchema, http_manager: http_manager_dep):
    r = await http_manager.post(
        f'{config.auth_service.url}/{config.auth_service.api_ver}/login', 
        user.model_dump()
    )
    response = JSONResponse(r.json(), r.status_code)
    for cookie in r.cookies.jar:
        response.set_cookie(cookie.name, cookie.value)
    return response