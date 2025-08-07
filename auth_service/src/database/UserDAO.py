from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.models import OrmUser


class UserDAO:
    async def get_by_id(self, db: AsyncSession, user_id: int) -> OrmUser | None:
        query = select(OrmUser).where(OrmUser.id == user_id)
        user = (await db.execute(query)).scalar_one_or_none()
        return user
    

    async def get_by_email(self, db: AsyncSession, email: str) -> OrmUser | None:
        query = select(OrmUser).where(OrmUser.email == email)
        user = (await db.execute(query)).scalar_one_or_none()
        return user
    

    async def create(self, db: AsyncSession, new_user: OrmUser) -> None:
        db.add(new_user)


    async def delete(self, db: AsyncSession, user_id: int) -> None:
        user = await self.get_by_id(db, user_id)
        await db.delete(user)
        
        