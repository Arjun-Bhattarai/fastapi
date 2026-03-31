from fastapi import Depends, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from typing import Any, List

from .utils import decode_access_token
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import AuthService
from .models import User

user_service = AuthService()


class AccessToken(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        token_data = decode_access_token(credentials.credentials)

        if await token_in_blocklist(token_data.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted",
            )

        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError


class AccessTokenBearer(AccessToken):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(AccessToken):
    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a refresh token",
            )


# ✅ FIXED: use UID instead of email
async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    db: AsyncSession = Depends(get_session),
) -> User:

    user_id = token_data.get("uid")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UID missing in token",
        )

    user = await user_service.get_user_by_id(user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> bool:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return True