from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime, timezone
from db import SessionLocal
from models import User, RefreshToken
from security import (
    hash_password,
    verify_password,
    make_access_token,
    make_refresh_token,
    decode_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access: str
    refresh: str | None = None
    token_type: str = "bearer"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenOut)
def register(body: RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == body.email)):
        raise HTTPException(409, "Email already registered")
    user = User(email=body.email, hashed_password=hash_password(body.password), name=body.name)
    db.add(user)
    db.flush()
    access = make_access_token(str(user.id))
    refresh, exp = make_refresh_token()
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=exp))
    db.commit()
    return TokenOut(access=access, refresh=refresh)

@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email))
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    access = make_access_token(str(user.id))
    refresh, exp = make_refresh_token()
    db.add(RefreshToken(user_id=user.id, token=refresh, expires_at=exp))
    db.commit()
    return TokenOut(access=access, refresh=refresh)

class RefreshIn(BaseModel):
    refresh: str

@router.post("/refresh", response_model=TokenOut)
def refresh_token(body: RefreshIn, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    row = db.scalar(select(RefreshToken).where(and_(RefreshToken.token == body.refresh, RefreshToken.revoked == False)))
    if not row or row.expires_at < now:
        raise HTTPException(401, "Invalid or expired refresh token")
    access = make_access_token(str(row.user_id))
    return TokenOut(access=access, refresh=None)

@router.post("/logout")
def logout(body: RefreshIn, db: Session = Depends(get_db)):
    row = db.scalar(select(RefreshToken).where(RefreshToken.token == body.refresh))
    if row:
        row.revoked = True
        db.commit()
    return {"ok": True}

# ще ни трябва за защитени маршрути по-нататък
def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(401, "Invalid token")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(401, "Invalid user")
    return user
