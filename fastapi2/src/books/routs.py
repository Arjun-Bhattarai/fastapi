from src.books.schemas import BookCreate, BookUpdate, BookRead
from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.books.service import BookService
from typing import List

router = APIRouter()
book_service = BookService()


@router.get("/", response_model=List[BookRead])
async def get_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(book_id: UUID, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_id, session)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book  # fixed: was return {"book": book}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookRead)
async def create_book(book: BookCreate, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_book(book, session)
    return new_book


@router.put("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: UUID, book: BookUpdate, session: AsyncSession = Depends(get_session)
):
    updated_book = await book_service.update_book(book_id, book, session)
    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return updated_book  # fixed: was return {"message": ..., "book": updated_book}


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, session: AsyncSession = Depends(get_session)):
    deleted = await book_service.delete_book(book_id, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )