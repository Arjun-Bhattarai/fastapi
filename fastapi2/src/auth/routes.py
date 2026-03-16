from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreate, user_model
from .service import AuthService
from src.db.main import get_session

auth_router = APIRouter()
user_service = AuthService()


@auth_router.post("/signup", response_model=user_model, status_code=status.HTTP_201_CREATED)
async def signup(
    user: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    email = user.email
    username = user.username

    user_exists = await user_service.user_exists(email, username, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    new_user = await user_service.create_user(user, session)
    return new_user