from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import OrmPaste


class PasteDAO:
    async def get_all_user_pastes(
        self,
        db: AsyncSession, 
        user_id: int,
        filters: list = None,
    ) -> list[OrmPaste]:
        query = select(OrmPaste).where(OrmPaste.owner_id == user_id)
        if filters:
            query = query.where(*filters)
        pastes = (await db.execute(query)).scalars().all()
        return pastes
    
    
    async def get_paste_by_public_url(
        self,
        db: AsyncSession,
        public_url: str,
        filters: list,
    ) -> OrmPaste | None:
        query = select(OrmPaste).where(OrmPaste.public_url == public_url)
        if filters:
            query = query.where(*filters)
        paste = (await db.execute(query)).scalar_one_or_none()
        return paste
    

    async def get_paste_by_id(
        self,
        db: AsyncSession, 
        user_id: int, 
        paste_id: int,
        filters: list = None,
    ) -> OrmPaste | None:
        query = select(OrmPaste).where(
            OrmPaste.owner_id == user_id,
            OrmPaste.id == paste_id,
        )
        if filters:
            query = query.where(*filters)
        paste = (await db.execute(query)).scalar_one_or_none()
        return paste
    
    
    async def add_paste(self, db: AsyncSession, paste: OrmPaste) -> None:
        db.add(paste)


    async def delete_paste(self, db: AsyncSession, paste: OrmPaste) -> None:
        await db.delete(paste)