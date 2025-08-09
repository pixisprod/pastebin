from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc
from passlib.context import CryptContext

from eventhub.pydantic.auth_service.UserSchema import UserSchema
from eventhub.kafka.producer.Producer import Producer
from eventhub.avro.AvroManager import AvroManager
from eventhub.confluent.ConfluentSRClient import ConfluentSRClient


from src.database.UserDAO import UserDAO
from src.models import OrmUser
from src.auth import exceptions


class ServiceInfra:
    def __init__(
        self,
        hasher: CryptContext,
        avro_manager: AvroManager,
        sr_client: ConfluentSRClient,
    ):
        self.hasher = hasher
        self.avro_manager = avro_manager
        self.sr_client = sr_client
        


class AuthService:
    def __init__(self, user_dao: UserDAO, kafka_producer: Producer):
        self.__user_dao = user_dao
        self.kafka_producer: Producer = kafka_producer

    
    async def register_user(
        self, 
        db: AsyncSession, 
        infra: ServiceInfra,
        user: UserSchema,
    ) -> int:
        new_user = OrmUser(**user.model_dump())
        new_user.password = infra.hasher.hash(new_user.password)
        await self.__user_dao.create(db, new_user)
        try:
            await db.commit()
        except exc.IntegrityError:
            await db.rollback()
            raise exceptions.UserAlreadyExistsException()
        except Exception:
            await db.rollback()
            raise 
        return new_user.id 


    async def login_user(
        self,
        credentials: UserSchema,
        db: AsyncSession,
        infra: ServiceInfra,
    ) -> OrmUser:
        user = await self.__user_dao.get_by_email(db, credentials.email)
        if not user or not infra.hasher.verify(credentials.password, user.password):
            raise exceptions.UserIncorrectCredentialsException
        return user
