import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, DateTime, Text, String


class OrmBase(DeclarativeBase):
    pass


class OrmPaste(OrmBase):
    __tablename__ = 'pastes'
    
    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    public_url: Mapped[str] = mapped_column(
        String(36),
        nullable=True,
        index=True,
        unique=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC),
    )
    expire_on: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=7)
    )