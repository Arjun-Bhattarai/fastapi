from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi import Header

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello this is fastapi2"}


@app.get("/greet")  # http link ma greet paxi name and age  parameter use garnu parxa
async def greet(
    name: Optional[str] = "user", age: Optional[int] = 0) -> dict:  # name and age parameter optional banako xa, default value user rakhako xa
    return {"message": f"Hello, {name},{age}! Welcome to FastAPI2!"}


class Book(BaseModel):
    title: str
    author: str


@app.post("/create_book")
async def create_book(book: Book):
    return {
        "title": book.title,
        "author": book.author,
    }


@app.get("/get_header")
async def get_header(
    accept: str = Header("None"),
    content_type: str = Header("None"),
    user_agent: str = Header("None"),
    host: str = Header("None")
):
    request_header = {}
    request_header["Accept"] = accept
    request_header["Content-Type"] = content_type
    request_header["User-Agent"] = user_agent
    request_header["Host"] = host
    return request_header
