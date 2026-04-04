from src.books.schemas import BookCreate, BookUpdate, BookRead
from uuid import UUID
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.books.service import BookService
from typing import List
from src.auth.dependency import AccessTokenBearer, RoleChecker

router = APIRouter()
book_service = BookService()

access_token = AccessTokenBearer()
role_checker = RoleChecker(["admin", "user"])


# ✅ Move this ABOVE /{book_id}
@router.get("/user/{user_id}", response_model=List[BookRead])
async def get_user_book_submission(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(role_checker),
):
    books = await book_service.get_user_books(user_id, session)
    return books


@router.get("/", response_model=List[BookRead])
async def get_books(
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(role_checker),
):
    return await book_service.get_all_books(session)


@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(role_checker),
):
    book = await book_service.get_book(book_id, session)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookRead)
async def create_book(
    book: BookCreate,
    session: AsyncSession = Depends(get_session),
    user=Depends(access_token),
):
    user_id = user.get("uid")

    return await book_service.create_book(book, session, user_id=user_id)


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: UUID,
    book: BookUpdate,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(role_checker),
):
    updated_book = await book_service.update_book(book_id, book, session)

    if not updated_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: UUID,
    session: AsyncSession = Depends(get_session),
    _: bool = Depends(role_checker),
):
    deleted = await book_service.delete_book(book_id, session)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )