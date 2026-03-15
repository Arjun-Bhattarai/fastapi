from uuid import UUID
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.models import Books
from src.books.schemas import BookCreate, BookUpdate
from datetime import datetime, timezone


def to_naive_utc(dt: datetime) -> datetime:
    if dt is not None and dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


class BookService:

    async def get_all_books(self, session: AsyncSession):
        result = await session.exec(select(Books))
        return result.all()

    async def get_book(self, book_id: UUID, session: AsyncSession):
        result = await session.exec(select(Books).where(Books.uid == book_id))
        return result.first()

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        data = book_data.model_dump()
        data["publish_date"] = to_naive_utc(data["publish_date"])  # ← safety net
        book = Books(**data)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def update_book(self, book_id: UUID, book_data: BookUpdate, session: AsyncSession):
        book = await self.get_book(book_id, session)
        if not book:
            return None
        for key, value in book_data.model_dump(exclude_unset=True).items():
            if isinstance(value, datetime):
                value = to_naive_utc(value)  
            setattr(book, key, value)
        book.update_at = datetime.utcnow()
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_id: UUID, session: AsyncSession):
        book = await self.get_book(book_id, session)
        if not book:
            return False
        await session.delete(book)
        await session.commit()
        return True