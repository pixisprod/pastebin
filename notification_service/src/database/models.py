import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime, Boolean


class OrmBase(DeclarativeBase):
    pass


class OrmTelegramChannel(OrmBase):
    __tablename__ = 'telegram'

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, 
        index=True, 
        nullable=False,
        unique=True,
    )
    telegram_id: Mapped[int] = mapped_column(
        Integer,
        index=True,
        unique=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(datetime.UTC)
    )
