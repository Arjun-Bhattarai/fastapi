from sqlalchemy import column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from ..db import Base

class todoschema(Base):
    __tablename__="todos"
    id=column(Integer, primary_key=True, index=True,autoincrement=True)
    content=column(String(500), nullable=False)
    is_completed=column(Boolean, default=False)
    created_at=column(String(100), nullable=False, default=datetime.now(timezone.utc))
    updated_at=column(String(100), nullable=False, default=datetime.now(timezone.utc))