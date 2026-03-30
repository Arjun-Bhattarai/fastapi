from fastapi import Depends, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_access_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import AuthService
from typing import Any, List
from .models import User

user_service = AuthService()


class AccessToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )
        token_data = decode_access_token(credentials.credentials)

        if await token_in_blocklist(token_data.get("jti")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is blacklisted",
            )

        self.verify_token_data(
            token_data
        )  # yo method le token data verify garne logic handle garxa, jaba token decode hunxa. Yo method lai AccessToken class ma define garna parxa, tara implementation AccessTokenBearer ra RefreshTokenBearer ma hunxa.

        return token_data

    def verify_token_data(
        self, token_data: dict
    ) -> (
        None
    ):  # yo method lai AccessToken class ma define garna parxa, tara implementation AccessTokenBearer ra RefreshTokenBearer ma hunxa. Yo method le token data verify garne logic handle garxa, jaba token decode hunxa.
        raise NotImplementedError("Subclasses must implement verify_token_data method")


class AccessTokenBearer(AccessToken):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(AccessToken):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a refresh token",
            )


async def get_current_user(
    token_data: dict = Depends(AccessTokenBearer()),
    db: AsyncSession = Depends(get_session),
) -> (
    dict
):  # yo function le current user ko data return garxa, jaba user request garcha. Yo function ma AccessTokenBearer dependency use garna parxa, jaba user request garcha, tyo bela token decode hunxa, token blocklist ma xa ki xaina check hunxa, token data verify hunxa, ani token data return hunxa. Yo function lai route handler ma use garna parxa, jaba user request garcha.
    user_email = token_data["email"]
    user = await user_service.get_user_by_email(user_email, db)
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
