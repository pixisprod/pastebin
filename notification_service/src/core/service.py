from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.codes import CodeGenerator
from src.core.messaging.producer import NotificationProducer
from src.database.DAO import TelegramChannelsDAO
from src.database.models import OrmTelegramChannel
from src.core import exceptions


class NotificationService:
    def __init__(
        self, 
        code_generator: CodeGenerator,
        producer: NotificationProducer,
        telegram_dao: TelegramChannelsDAO,
    ):
        self.__generator = code_generator
        self.__producer = producer
        self.__telegram_dao = telegram_dao


    async def telegram_set_code(self, redis: Redis, user_id: int) -> str:
        code = self.__generator.generate_code()
        await redis.set(f'tg_code:{code}', user_id, ex=300)
        return code
    

    async def telegram_confirm_code(
        self,
        db: AsyncSession,
        redis: Redis, 
        code: str, 
        telegram_uid: int,
    ):
        code_key = f'tg_code:{code}'
        user_id: bytes = await redis.get(code_key)
        if not user_id:
            raise exceptions.WrongCodeException()
        channel = OrmTelegramChannel(
            owner_id=int(user_id),
            telegram_id=telegram_uid,
        )
        await self.__telegram_dao.add(db, channel)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
    
    
    async def get_user_telegram(self, db: AsyncSession, user_id: int) -> int:
        channel = await self.__telegram_dao.get_channel_by_user_id(db, user_id)
        if not channel:
            raise exceptions.ChannelNotFoundException()
        telegram_id = channel.telegram_id
        return telegram_id


    async def is_telegram_linked(self, db: AsyncSession, telegram_id: int) -> bool:
        channel = await self.__telegram_dao.get_channel_by_telegram_id(
            db=db,
            telegram_uid=telegram_id,
        )
        if not channel:
            return False
        return True
            
        

    async def send_by_telegram(self, user_id: int, message: str) -> None:
        # telegram_id = 
        await self.__producer.send_telegram(
            telegram_user_id=user_id,
            message=message,
        )