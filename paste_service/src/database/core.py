from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)

from src.config import Settings
from src.database.models import OrmBase


config = Settings.load()


DATABASE_URL_PARAMETERS = f'{config.db.user.get_secret_value()}:{config.db.password.get_secret_value()}@{config.db.host}/{config.db.name}'
DATABASE_URL = f'postgresql+asyncpg://{DATABASE_URL_PARAMETERS}'

engine = create_async_engine(DATABASE_URL)

session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db():
    async with session_factory() as db:
        yield db


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(OrmBase.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(OrmBase.metadata.drop_all)
