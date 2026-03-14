from uuid import UUID
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone


def normalize_datetime(v):
    if v is None:
        return v
    if isinstance(v, str):
        v = datetime.fromisoformat(v)
    if isinstance(v, datetime) and v.tzinfo is not None:
        return v.astimezone(timezone.utc).replace(tzinfo=None)
    return v


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: datetime
    page_count: int
    language: str

    @field_validator("publish_date", mode="before")
    @classmethod
    def strip_timezone(cls, v):
        return normalize_datetime(v)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
    publish_date: datetime | None = None
    page_count: int | None = None
    language: str | None = None

    @field_validator("publish_date", mode="before")
    @classmethod
    def strip_timezone(cls, v):
        return normalize_datetime(v)


class BookRead(BookBase):
    uid: UUID
    create_at: datetime
    update_at: datetime