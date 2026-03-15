from fastapi import APIRouter
from .schemas import UserCreate

auth_router = APIRouter()

@auth_router.post("/signup")
async def signup(user: UserCreate):
    return {"message": "Signup endpoint", "user": user}