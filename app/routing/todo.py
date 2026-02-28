
from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
router=APIRouter(prefix="/todo")

@router.get("/")
def index():
    return {"message":f"hello what are you doing"}


@router.post("")
def store(item:CreateTodo):
    return {"message":"todo created ", "item": item.model_dump()}

