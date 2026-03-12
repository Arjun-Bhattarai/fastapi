from uuid import uuid4

from pydantic import BaseModel
from datetime import datetime

class Books(BaseModel):
    uid: uuid4
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreate(BaseModel):
    title: str 
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str
    created_at: datetime

class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
    updated_at: datetime
