from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List

class Books(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publish_date: str
    page_count: int
    language: str


class UpdateBooks(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


app = FastAPI()

books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Scribner",
        "publish_date": "1925",
        "page_count": 218,
        "language": "English",
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J.B. Lippincott & Co.",
        "publish_date": "1960",
        "page_count": 281,
        "language": "English",
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "publisher": "Secker & Warburg",
        "publish_date": "1948",
        "page_count": 328,
        "language": "English",
    },
]


@app.get("/books", response_model=List[Books])
async def get_books():
    return books


@app.get("/books/{book_id}")
async def get_book(book_id: int):
    book = next((book for book in books if book["id"] == book_id), None)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return {"book": book}


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book: Books):
    new_book = book.model_dump()
    books.append(new_book)

    return {
        "message": "Book created successfully",
        "book": new_book
    }


@app.put("/books/{book_id}")
async def update_book(book_id: int, book: UpdateBooks):

    for index, existing_book in enumerate(books):

        if existing_book["id"] == book_id:

            updated_book = book.model_dump()
            updated_book["id"] = book_id
            updated_book["publish_date"] = existing_book["publish_date"]

            books[index] = updated_book

            return {
                "message": "Book updated successfully",
                "book": updated_book
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )


@app.delete("/books/{book_id}")
async def delete_book(book_id: int):

    for index, existing_book in enumerate(books):

        if existing_book["id"] == book_id:
            del books[index]

            return {"message": "Book deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )