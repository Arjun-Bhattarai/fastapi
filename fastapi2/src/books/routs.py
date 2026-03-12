from fastapi import FastAPI, APIRouter, status, HTTPException
from src.books.book_data import books
from src.books.schemas import Books, BookUpdate  # <- Use BookUpdate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Books])
async def get_books():
    return books

@router.get("/{book_id}")
async def get_book(book_id: int):
    book = next((book for book in books if book["id"] == book_id), None)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    return {"book": book}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Books):
    new_book = book.model_dump()
    books.append(new_book)

    return {"message": "Book created successfully", "book": new_book}

@router.put("/{book_id}")
async def update_book(book_id: int, book: BookUpdate):  # <- Use BookUpdate

    for index, existing_book in enumerate(books):

        if existing_book["id"] == book_id:

            updated_book = book.model_dump()
            updated_book["id"] = book_id
            updated_book["publish_date"] = existing_book["publish_date"]

            books[index] = updated_book

            return {"message": "Book updated successfully", "book": updated_book}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@router.delete("/{book_id}")
async def delete_book(book_id: int):

    for index, existing_book in enumerate(books):

        if existing_book["id"] == book_id:
            del books[index]

            return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")