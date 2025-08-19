import uuid
import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Select



from src.models import OrmPaste
from src.paste import exceptions


class PasteRepository:
    async def update_paste(
        self,
        new_paste_data: PasteEditSchema,
        paste_id: int,
        user_id: int,
        db: AsyncSession
    ) -> OrmPaste:
        paste = await self.get_paste(user_id, paste_id, db)
        data = new_paste_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(paste, key, value)
        try:
            await db.commit()
            return paste
        except Exception:
            await db.rollback()
            raise

    

    async def delete_paste(
        self,
        db: AsyncSession,
        user_id: int,
        paste_id: int,
    ) -> int:
        paste = await self.get_paste(user_id, paste_id, db)
        await db.delete(paste)
        try:
            await db.commit()
            return paste.id
        except Exception:
            await db.rollback()
            raise


    async def add_paste(
        self, 
        user_id: int,
        paste: PasteSchema,
        db: AsyncSession,
    ) -> int:
        new_paste = OrmPaste(**paste.model_dump(include={'content'}))
        new_paste.owner_id = user_id
        now = datetime.datetime.now(datetime.UTC)
        new_paste.expire_on = now + datetime.timedelta(seconds=paste.lifetime_seconds)
        db.add(new_paste)
        try:
            await db.flush()
            new_paste_id = new_paste.id
            await db.commit()
            return new_paste_id
        except Exception:
            await db.rollback()
            raise
    

    def __base_query(
        self, 
        user_id: int
    ) -> Select:
        now = datetime.datetime.now(datetime.UTC)
        query = select(OrmPaste).where(
            OrmPaste.owner_id == user_id,
            OrmPaste.expire_on > now,
        )
        return query
    

    async def get_pastes(
        self,
        user_id: int,
        db: AsyncSession,
    ) -> list[OrmPaste]:
        query = self.__base_query(user_id)
        pastes = (await db.execute(query)).scalars().all()
        return pastes
    

    async def get_public_paste(
        self,
        public_url: str,
        db: AsyncSession,
    ) -> OrmPaste:
        now = datetime.datetime.now(datetime.UTC)
        query = select(OrmPaste).where(
            OrmPaste.public_url != None,
            OrmPaste.public_url == public_url,
            OrmPaste.expire_on > now,
        )
        paste = (await db.execute(query)).scalar_one_or_none()
        if not paste:
            raise exceptions.PasteNotFoundException()
        return paste


    async def get_paste(
        self,
        user_id: int,
        paste_id: int,
        db: AsyncSession,
    ) -> OrmPaste:
        query = self.__base_query(user_id).where(OrmPaste.id == paste_id)
        paste = (await db.execute(query)).scalar_one_or_none()
        if not paste:
            raise exceptions.PasteNotFoundException()
        return paste


    async def _is_public_url_available(
        self,
        public_url: str, 
        db: AsyncSession,
    ) -> bool:
        now = datetime.datetime.now(datetime.UTC)
        query = select(OrmPaste).where(OrmPaste.public_url == public_url)
        check_paste_url = (await db.execute(query)).scalar_one_or_none()
        if check_paste_url:
            if check_paste_url.expire_on < now:
                await db.delete(check_paste_url)
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
        uid: int, 
        pid: int, 
        db: AsyncSession,
        public_url: str = None,
    ) -> str:
        if public_url:
            if not await self._is_public_url_available(public_url, db):
                raise exceptions.PublicUrlAlreadyExistsException()
        paste = await self.get_paste(uid, pid, db)
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
