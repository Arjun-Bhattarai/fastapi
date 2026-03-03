from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo, TodoSchema
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/todo")

@router.get("/")
def index():
    return {"message": "hello what are you doing"}

@router.post("/")
def store(item: CreateTodo, bd: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    bd.add(todo)
    bd.commit()
    bd.refresh(todo)
    return {"message": "todo created", "item": {"id": todo.id, "content": todo.content, "is_completed": todo.is_completed}}