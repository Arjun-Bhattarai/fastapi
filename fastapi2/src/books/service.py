from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreate, BookUpdate
from sqlmodel import select, desc
from .models import Books


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Books).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_id: int, session: AsyncSession):
        statement = select(Books).where(Books.uid == book_id)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self, book_data: BookCreate, session: AsyncSession):
        new_book = Books(**book_data.model_dump())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_id: int, book_data: BookUpdate, session: AsyncSession):
        statement = select(Books).where(Books.uid == book_id)
        result = await session.exec(statement)
        book = result.first()

        if book is None:
            return None

        for key, value in book_data.model_dump(exclude_unset=True).items():
            setattr(book, key, value)

        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_id: int, session: AsyncSession):
        statement = select(Books).where(Books.uid == book_id)
        result = await session.exec(statement)
        book = result.first()

        if book is None:
            return None

        await session.delete(book)
        await session.commit()
        return book