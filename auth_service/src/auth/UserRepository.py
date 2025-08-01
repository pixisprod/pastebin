from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc, select

from schemas_lib.auth_service.UserSchema import UserSchema

from src.models import OrmUser
from src.auth import exceptions
from src.auth.security.bcrypt import bcrypt_context
from src.auth.security.JwtManager import JwtManager

class UserRepository:
    async def login_user(self, user: UserSchema, db: AsyncSession):
        query = select(OrmUser).where(OrmUser.email == user.email)
        result = (await db.execute(query)).scalar_one_or_none()
        if not result or not bcrypt_context.verify(user.password, result.password):
            raise exceptions.UserIncorrectCredentialsException()
        return result

    async def create_user(self, user: UserSchema, db: AsyncSession) -> int:
        new_user = OrmUser(**user.model_dump())
        new_user.password = bcrypt_context.hash(new_user.password)
        db.add(new_user)
        try:
            await db.flush()
            user_id = new_user.id
            await db.commit()
            return user_id
        except exc.IntegrityError:
            await db.rollback()
            raise exceptions.UserAlreadyExistsException()
        except Exception:
            await db.rollback()
            raise
    
    @classmethod
    def load(cls):
        return cls()
    