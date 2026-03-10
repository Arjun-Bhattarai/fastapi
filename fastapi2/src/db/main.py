from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from src.config import config

engine = AsyncEngine(create_async_engine(config.DATABASE_URL, echo=True))

