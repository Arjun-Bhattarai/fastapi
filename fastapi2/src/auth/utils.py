from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from src.config import config
import uuid
import logging

password_context = CryptContext(
    schemes=["bcrypt"]
)  
ACCESS_TOKEN_EXPIRE = 3600


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: int = 3600, refresh_token: bool = False) -> str:
    # JWT token create garne function, yo function le user data lai token ma encode garxa, tyo token le user ko identity prove garxa, tyo token expire hune time pani set garna milxa.
    payload = {}
    payload.update(data)
    payload["user_id"] = data.get("user_id")
    payload["exp"] = (
        datetime.now(timezone.utc) + timedelta(seconds=expires_delta)  
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE)
    )
    payload["jti"] = str(uuid.uuid4())  # Unique identifier for the token, token lai unique banauxa
    payload["refresh"] = refresh_token  # refresh token ho ki access token ho bhanera identify garna

    token = jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    try:
        token_data = jwt.decode(jwt=token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None 
    return token_data