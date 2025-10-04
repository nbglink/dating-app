from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import jwt, JWTError
from datetime import datetime, timezone
import os

from db import SessionLocal
from models import User

router = APIRouter(prefix="/users", tags=["users"])

JWT_SECRET = os.getenv("API_SECRET", "dev-secret")
JWT_ALG = "HS256"

class MeOut(BaseModel):
    id: int
    email: str
    name: str | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(401, "Invalid token")
        # опит за прост expiry check (ако exp липсва, jose ще хвърли изключение)
        exp = payload.get("exp")
        if exp and datetime.now(timezone.utc).timestamp() > float(exp):
            raise HTTPException(401, "Token expired")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = db.scalar(select(User).where(User.id == int(sub)))
    if not user:
        raise HTTPException(401, "Invalid user")
    return user

@router.get("/me", response_model=MeOut)
def me(user: User = Depends(get_current_user)):
    return MeOut(id=user.id, email=user.email, name=getattr(user, "name", None))
