from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class TodoSchema(Base):
    __tablename__ = "todo"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(String(100), nullable=False, default=datetime.now(timezone.utc))
    updated_at = Column(String(100), nullable=False, default=datetime.now(timezone.utc))