from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import Optional

class Books(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    publish_date: datetime
    page_count: int
    language: str
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    create_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow)
    )
    update_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow)
    )

    def __repr__(self) -> str:
        return f"Books(title={self.title})"