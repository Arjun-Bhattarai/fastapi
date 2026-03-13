from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.schemas import Books, BookUpdate
from typing import List
from src.db.main import get_session
from src.books.service import BookService

router = APIRouter()
book_service = BookService()


@router.get("/", response_model=List[Books])#response_model le API response lai List[Books] type ma convert garxa
async def get_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@router.get("/{book_id}")
async def get_book_by_id(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_id, session)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {"book": book}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Books, session: AsyncSession = Depends(get_session)):#Depends(get_session) le get_session function lai call garxa ra AsyncSession object provide garxa
    new_book = await book_service.create_book(book, session)

    return {"message": "Book created successfully", "book": new_book}


@router.put("/{book_id}")
async def update_book(
    book_id: int, book: BookUpdate, session: AsyncSession = Depends(get_session)
):
    updated_book = await book_service.update_book(book_id, book, session)

    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {"message": "Book updated successfully", "book": updated_book}


@router.delete("/{book_id}")
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await book_service.delete_book(book_id, session)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {"message": "Book deleted successfully"}