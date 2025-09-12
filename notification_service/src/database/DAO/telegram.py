from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import OrmTelegramChannel


class TelegramChannelsDAO:
    async def add(self, db: AsyncSession, channel: OrmTelegramChannel):
        db.add(channel)


    async def get_channel_by_user_id(
        self, 
        db: AsyncSession, 
        user_id: int,
    ) -> OrmTelegramChannel | None:        
        query = select(OrmTelegramChannel).where(
            OrmTelegramChannel.owner_id == user_id,
        )
        result = (await db.execute(query)).scalar_one_or_none()
        return result

    
    async def get_channel_by_telegram_id(
        self, 
        db: AsyncSession, 
        telegram_uid: int
    ) -> OrmTelegramChannel | None:
        query = select(OrmTelegramChannel).where(
            OrmTelegramChannel.telegram_id == telegram_uid,
        )
        channel = (await db.execute(query)).scalar_one_or_none()
        return channel