import datetime

from pydantic import BaseModel, ConfigDict, Field
from src.config import Settings


config = Settings.load()


class PasteSchema(BaseModel):
    content: str = Field(
        min_length=config.paste.content_min_length,
        max_length=config.paste.content_max_length,
        examples=['Example paste for docs..'],
    )
    lifetime_seconds: int = Field(
        ge=config.paste.lifetime_min_seconds,
        le=config.paste.lifetime_max_seconds,
    )

class PasteEditSchema(BaseModel):
    content: str = Field(
        min_length=config.paste.content_min_length,
        max_length=config.paste.content_max_length,
        examples=['Updated paste for docs..'],
    )

class PastePublishSchema(BaseModel):
    public_url: str = Field(
        min_length=config.paste.public_url_min_length, 
        max_length=config.paste.public_url_max_length, 
        default=None,
        examples=['viral-public-url']
    )


class PasteOut(BaseModel):
    id: int
    content: str
    public_url: str | None
    created_at: datetime.datetime
    expire_on: datetime.datetime

    model_config = ConfigDict(from_attributes=True)