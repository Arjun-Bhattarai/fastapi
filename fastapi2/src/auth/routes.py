from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from .schemas import UserCreate, user_model, UserLogin
from .service import AuthService
from src.db.main import get_session
from .utils import create_access_token, verify_password
from .dependency import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = AuthService()

refresh_token_expires_delta = 3600 * 24 * 7
role_checker = RoleChecker(["admin", "user"])



@auth_router.post("/signup", response_model=user_model)
async def signup(user: UserCreate, session: AsyncSession = Depends(get_session)):

    if await user_service.user_exists(user.email, user.username, session):
        raise HTTPException(400, "User already exists")

    return await user_service.create_user(user, session)



@auth_router.post("/login")
async def login_users(user: UserLogin, session: AsyncSession = Depends(get_session)):

    db_user = await user_service.get_user_by_email(user.email, session)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token(
        data={
            "uid": str(db_user.uid),
            "email": db_user.email,
            "username": db_user.username,
            "role": db_user.role,
        }
    )

    refresh_token = create_access_token(
        data={
            "uid": str(db_user.uid),
            "email": db_user.email,
            "username": db_user.username,
            "role": db_user.role,
        },
        expires_delta=refresh_token_expires_delta,
        refresh_token=True,
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "email": db_user.email,
            "username": db_user.username,
        },
    }


@auth_router.get("/refresh")
async def refresh_token(credentials=Depends(RefreshTokenBearer())):

    if datetime.fromtimestamp(credentials["exp"], tz=timezone.utc) <= datetime.now(timezone.utc):
        raise HTTPException(400, "Refresh token expired")

    new_access_token = create_access_token(
        data={
            "uid": credentials.get("uid"),
            "email": credentials.get("email"),
            "username": credentials.get("username"),
            "role": credentials.get("role"),
        }
    )

    return {
        "message": "Token refreshed successfully",
        "access_token": new_access_token,
    }



@auth_router.get("/me")
async def me(
    user=Depends(get_current_user),
    _: bool = Depends(role_checker),
):
    return user


@auth_router.get("/logout")
async def logout(credentials=Depends(AccessTokenBearer())):

    jti = credentials.get("jti")

    if jti:
        await add_jti_to_blocklist(jti)

    return {
        "message": "Logout successful"
    }