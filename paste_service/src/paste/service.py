import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.paste.schemas import (
    PasteSchema, PasteEditSchema
)
from src.database.PasteDAO import PasteDAO
from src.models import OrmPaste
from src.paste import exceptions


class PasteService:
    def __init__(self, paste_dao: PasteDAO):
        self.__paste_dao = paste_dao

    
    def __get_default_filters(self) -> list:
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
            filters=self.__get_default_filters()
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
            filters=self.__get_default_filters()
        )
        if not paste:
            raise exceptions.PasteNotFoundException()
        return paste
    

    async def get_public_paste(self, db: AsyncSession, url: str) -> OrmPaste:
        paste = await self.__paste_dao.get_paste_by_public_url(
            db=db,
            public_url=url,
            filters=self.__get_default_filters()
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


    async def edit_paste(
        self,
        user_id: int,
        paste_id: int,
        db: AsyncSession,
        upd_paste_data: PasteEditSchema,
    ) -> OrmPaste:
        paste = await self.get_paste(db, user_id, paste_id)
        new_data = upd_paste_data.model_dump(exclude_unset=True)
        for key, value in new_data.items():
            setattr(paste, key, value)
        try:
            await db.commit()
            return paste
        except Exception:
            await db.rollback()
            raise
        

    async def _is_public_url_available(
        self,
        public_url: str,
        db: AsyncSession,
    ) -> bool:
        check_paste_url = await self.__paste_dao.get_paste_by_public_url(
            db=db,
            public_url=public_url,
        )
        now = datetime.datetime.now(datetime.UTC)
        if check_paste_url:
            if check_paste_url.expire_on < now:
                await self.__paste_dao.delete_paste(db, check_paste_url)
                try:
                    await db.commit()
                except Exception:
                    await db.rollback()
                    raise
                return True
            return False
        return True
    

    async def publish_paste(
        self, 
        user_id: int, 
        paste_id: int,
        db:  AsyncSession,
        public_url: str = None,
    ) -> str:
        if public_url:
            if not await self._is_public_url_available(public_url, db):
                raise exceptions.PublicUrlAlreadyExistsException()
        paste = await self.get_paste(db, user_id, paste_id)
        if not public_url:
            paste.public_url = str(uuid.uuid4())
        else:
            paste.public_url = public_url
        try:
            await db.commit()
            return paste.public_url
        except Exception:
            await db.rollback()
            raise
        
        