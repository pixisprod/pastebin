from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.database.core import get_db


db_dep = Annotated[AsyncSession, Depends(get_db)]