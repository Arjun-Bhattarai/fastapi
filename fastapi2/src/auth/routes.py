from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreate, user_model, UserLogin
from .service import AuthService
from src.db.main import get_session
from .utils import create_access_token, decode_access_token, verify_password
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse

auth_router = APIRouter()
user_service = AuthService()

refresh_token_expires_delta = 3600 * 24 * 7  


@auth_router.post(
    "/signup", response_model=user_model, status_code=status.HTTP_201_CREATED
)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_session)):
    email = user.email
    username = user.username

    user_exists = await user_service.user_exists(email, username, session)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )

    new_user = await user_service.create_user(user, session)
    return new_user


@auth_router.post("/login")
async def login_users(user: UserLogin, session: AsyncSession = Depends(get_session)):
    email = user.email
    password = user.password

    db_user = await user_service.get_user_by_email(
        email, session
    )  # yo function le email ko basis ma user lai database bata fetch garxa, jaba user login garna try garcha, tyo bela email ko basis ma user data fetch hunxa.

    if not db_user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    password_valid = verify_password(password, db_user.password) 

    if not password_valid: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    access_token = create_access_token(  
        data={"email": db_user.email, "username": db_user.username}  
    )

    refresh_token = create_access_token(  # refresh token create garne, yo token le access token expire bhayepachi naya access token lina use garxa
        data={"email": db_user.email, "username": db_user.username},  
        expires_delta=refresh_token_expires_delta,
        refresh_token=True,
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": db_user.email,
                "username": db_user.username,
            },
        }
    )