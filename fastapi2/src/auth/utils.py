from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import jwt
import uuid
from src.config import config

password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRE = 3600
REFRESH_TOKEN_EXPIRE = 86400 * 7


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: int = ACCESS_TOKEN_EXPIRE,
    refresh_token: bool = False,
) -> str:
    payload = {
        **data,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_delta),
        "jti": str(uuid.uuid4()),
        "refresh": refresh_token,
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )