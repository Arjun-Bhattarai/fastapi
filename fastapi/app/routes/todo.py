from fastapi import APIRouter, Depends
import sqlalchemy
from app.models.todo import CreateTodo, TodoSchema
from typing import Annotated
from sqlalchemy.orm import Session
from app.database import get_db
from sqlalchemy import select
from app.dependencies import authenticate_user
from app.models.auth import authuser


router = APIRouter(dependencies=[Depends(authenticate_user)])


@router.get("/")
def index(db: Annotated[Session, Depends(get_db)],authuser: Annotated[authuser, Depends(authenticate_user)]):

    todos = db.query(TodoSchema).all()
    stmt = select(TodoSchema.id, TodoSchema.content, TodoSchema.is_completed)
    todos = db.execute(stmt).mappings().all()
    return {"message": "hello what are you doing", "todos": todos, "authuser": authuser}


@router.post("/")
def store(item: CreateTodo, bd: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    bd.add(todo)
    bd.commit()
    bd.refresh(todo)
    return {
        "message": "todo created",
        "item": {
            "id": todo.id,
            "content": todo.content,
            "is_completed": todo.is_completed,
        },
    }


@router.get("/{id}")
def show(id: int, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "todo not found"}
    return {
        "message": "todo found",
        "item": {
            "id": todo.id,
            "content": todo.content,
            "is_completed": todo.is_completed,
        },
    }


@router.delete("/{id}")
def delete(id: int, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "todo not found"}
    db.delete(todo)
    db.commit()
    return {"message": "todo deleted"}


@router.put("/{id}")
def update(id: int, item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "todo not found"}
    todo.content = item.content
    todo.is_completed = item.is_completed
    db.commit()
    db.refresh(todo)
    return {
        "message": "todo updated",
        "item": {
            "id": todo.id,
            "content": todo.content,
            "is_completed": todo.is_completed,
        },
    }