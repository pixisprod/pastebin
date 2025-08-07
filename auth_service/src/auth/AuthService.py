from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from passlib.context import CryptContext

from eventhub.pydantic.auth_service.UserSchema import UserSchema

from src.database.UserDAO import UserDAO
from src.models import OrmUser
from src.auth import exceptions


class AuthService:
    def __init__(self, user_dao: UserDAO):
        self.__user_dao: UserDAO = user_dao

    
    async def register_user(
        self, 
        db: AsyncSession, 
        user: UserSchema,
        hasher: CryptContext
    ) -> int:
        new_user = OrmUser(**user.model_dump())
        new_user.password = hasher.hash(new_user.password)
        await self.__user_dao.create(db, new_user)
        try:
            await db.commit()
            return new_user.id
        except exc.IntegrityError:
            await db.rollback()
            raise exceptions.UserAlreadyExistsException()
        except Exception:
            await db.rollback()
            raise   


    async def login_user(
        self,
        credentials: UserSchema,
        db: AsyncSession,
        hasher: CryptContext,
    ) -> OrmUser:
        user = await self.__user_dao.get_by_email(db, credentials.email)
        if not user or not hasher.verify(credentials.password, user.password):
            raise exceptions.UserIncorrectCredentialsException
        return user
