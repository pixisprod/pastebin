import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select

from eventhub.pydantic.paste_service.PasteSchema import PasteSchema

from src.database.PasteDAO import PasteDAO
from src.models import OrmPaste
from src.paste import exceptions


class PasteService:
    def __init__(self, paste_dao: PasteDAO):
        self.__paste_dao = paste_dao

    
    async def __get_default_filters(self) -> list:
        filters = []
        now = datetime.datetime.now(datetime.UTC)
        paste_not_expired = OrmPaste.expire_on > now

        filters.append(paste_not_expired)
        return filters
    

    async def get_pastes(
        self, 
        db: AsyncSession,
        user_id: int
    ) -> list[OrmPaste]:
        pastes = await self.__paste_dao.get_all_user_pastes(
            db=db, 
            user_id=user_id, 
            filters=await self.__get_default_filters()
        )
        return pastes
    

    async def get_paste(
        self,
        db: AsyncSession,
        user_id: int,
        paste_id: int,
    ) -> OrmPaste:
        paste = await self.__paste_dao.get_paste_by_id(
            db=db,
            user_id=user_id,
            paste_id=paste_id,
            filters=await self.__get_default_filters()
        )
        if not paste:
            raise exceptions.PasteNotFoundException()
        return paste
    

    async def add_paste(
        self,
        db: AsyncSession,
        user_id: int,
        paste: PasteSchema,
    ) -> int:
        to_add = OrmPaste(**paste.model_dump(include={'content'}))
        to_add.owner_id = user_id
        now = datetime.datetime.now(datetime.UTC)
        to_add.expire_on = now + datetime.timedelta(seconds=paste.lifetime_seconds)
        await self.__paste_dao.add_paste(db, to_add)
        try:
            await db.commit()
            return to_add.id
        except Exception:
            await db.rollback()
            raise

    
    async def delete_paste(
        self,
        user_id: int,
        paste_id: int,
        db: AsyncSession,
    ) -> int:
        to_delete = await self.get_paste(db, user_id, paste_id)
        await self.__paste_dao.delete_paste(db, to_delete)
        try:
            await db.commit()
            return to_delete.id
        except Exception:
            await db.rollback()
            raise