import datetime

from pydantic import BaseModel, ConfigDict


class PasteOut(BaseModel):
    id: int
    content: str
    public_url: str | None
    created_at: datetime.datetime
    expire_on: datetime.datetime

    model_config = ConfigDict(from_attributes=True)