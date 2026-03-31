from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreate, user_model, UserLogin
from .service import AuthService
from src.db.main import get_session
from .utils import create_access_token, verify_password
from fastapi.responses import JSONResponse
from .dependency import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from datetime import datetime, timedelta, timezone
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = AuthService()

refresh_token_expires_delta = 3600 * 24 * 7
role_checker = RoleChecker(["admin","user"])


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
        data={"email": db_user.email, "username": db_user.username, "role": db_user.role}
    )

    refresh_token = create_access_token(  # refresh token create garne, yo token le access token expire bhayepachi naya access token lina use garxa
        data={"email": db_user.email, "username": db_user.username, "role": db_user.role},
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


@auth_router.get(
    "/refresh"
)  # yo endpoint le refresh token lai access token ma convert garne, jaba access token expire bhayepachi naya access token lina use garxa. Yo endpoint ma refresh token provide garna parxa, tyo refresh token valid xa ki nai check garne, ani valid bhaye naya access token create garne.
async def refresh_token(
    credentials=Depends(RefreshTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    expiry_timestamp = credentials.get("exp")

    if datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc) > datetime.now(
        timezone.utc
    ):
        new_access_token = create_access_token(
            data={
                "email": credentials.get("email"),
                "username": credentials.get("username"),
                "role": credentials.get("role"),
            }
        )
        return JSONResponse(
            content={
                "message": "Token refreshed successfully",
                "access_token": new_access_token,
            }
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token has expired"
    )


@auth_router.get("/me")
async def get_current_user(user=Depends(get_current_user), _:bool=Depends(role_checker)):
    return user


@auth_router.get("/logout")
async def revoke_token(credentials=Depends(AccessTokenBearer())):
    jti = credentials.get("jti")
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={"message": "Logout successful, token revoked"},
        status_code=status.HTTP_200_OK,
    )
