from sqlmodel import SQLModel,Field,Column #SQLModel le SQLAlchemy ko ORM lai extend garxa, Field le model ko field haru define garna use garxa
import sqlalchemy.dialects.postgresql as pg 
from datetime import datetime
import uuid
class Books(SQLModel,table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4))#primary_key=True le uid lai primary key banauxa, default=uuid.uuid4 le default value set garxa
    title: str
    author: str
    publisher: str
    publish_date: datetime
    page_count: int
    language: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

def __repr__(self) -> str:
    return f"Books( title={self.title})"