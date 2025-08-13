import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from passlib.context import CryptContext

from eventhub.pydantic.auth_service.UserSchema import UserSchema
from eventhub.topics import AuthTopics


from src.database.UserDAO import UserDAO
from src.models import OrmUser
from src.auth import exceptions
from src.auth.security.JwtManager import JwtManager
from src.auth.UserEventsPublisher import UserEventsPublisher


class AuthService:
    def __init__(
            self, 
            user_dao: UserDAO, 
            hasher: CryptContext,
            event_publisher: UserEventsPublisher,
    ):
        self.__user_dao = user_dao
        self.__hasher = hasher
        self.event_publisher = event_publisher 
    

    async def register_user(
        self, 
        db: AsyncSession, 
        user: UserSchema,
    ) -> int:
        new_user = OrmUser(**user.model_dump())
        new_user.password = self.__hasher.hash(new_user.password)
        await self.__user_dao.create(db, new_user)
        try:
            await db.commit()
        except exc.IntegrityError:
            await db.rollback()
            raise exceptions.UserAlreadyExistsException()
        except Exception:
            await db.rollback()
            raise
        topic = AuthTopics.UserRegistered
        await self.event_publisher.publish_registered(
            user_id=new_user.id,
            user_email=new_user.email,
            topic=str(topic),
        )
        return new_user.id 


    async def login_user(
        self,
        credentials: UserSchema,
        db: AsyncSession,
    ) -> OrmUser:
        user = await self.__user_dao.get_by_email(db, credentials.email)
        if not user or not self.__hasher.verify(credentials.password, user.password):
            raise exceptions.UserIncorrectCredentialsException()
        return user
    

    async def refresh_token(
        self, 
        token: str,
        now: datetime.datetime,
        db: AsyncSession,
        jwt_manager: JwtManager,
    ) -> str:
        payload = jwt_manager.decode_token(token)
        user_id = int(payload['sub'])
        user: OrmUser = await self.__user_dao.get_by_id(db, user_id)
        if not user:
            raise exceptions.UserNotFoundException()
        return jwt_manager.create_access_token(user.id, now)