import os, secrets
from datetime import datetime, timedelta, timezone
from typing import Tuple
from jose import jwt
from passlib.context import CryptContext

JWT_SECRET = os.getenv("API_SECRET", "dev-secret")
JWT_ALG = "HS256"
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN", "30"))
REFRESH_TTL_DAYS = int(os.getenv("REFRESH_TTL_DAYS", "30"))

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(raw: str) -> str:
    return pwd.hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    return pwd.verify(raw, hashed)

def make_access_token(sub: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ACCESS_TTL_MIN)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

def make_refresh_token() -> Tuple[str, datetime]:
    token = secrets.token_urlsafe(64)
    exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TTL_DAYS)
    return token, exp
