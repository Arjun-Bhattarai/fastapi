from pwdlib import PasswordHash
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config.app_config import get_app_config


def hash_password(password: str) -> str:
    hasher = PasswordHash.recommended()
    return hasher.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    hasher = PasswordHash.recommended()
    return hasher.verify(password, password_hash)

def create_access_token(data: dict, expiresInMinutes:int=30) -> str:
    config = get_app_config()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiresInMinutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.ALGORITHM or "HS256")
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    config = get_app_config()
    payload = jwt.decode(token, config.secret_key, algorithms=[config.ALGORITHM or "HS256"])
    return payload