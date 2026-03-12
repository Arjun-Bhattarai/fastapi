from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import text, create_engine,SQLModel
from src.config import config
from src.books.models import Books
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(create_engine(config.DATABASE_URL, echo=True))

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()->AsyncSession:
    Session=sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
