from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean
from app.database.db import Base

class CreateTodo(BaseModel):
    content: str = Field(..., max_length=500, min_length=5)
    is_completed: Optional[bool] = False

class TodoSchema(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)