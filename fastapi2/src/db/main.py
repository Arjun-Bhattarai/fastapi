from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import text, create_engine,SQLModel
from src.config import config
from src.books.models import Books

engine = AsyncEngine(create_engine(config.DATABASE_URL, echo=True))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

       