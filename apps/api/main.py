from fastapi import FastAPI
from sqlalchemy import text
from db import engine
from auth import router as auth_router
from users import router as users_router
from photos import router as photos_router

app = FastAPI(title="Dating API", version="0.2.0")
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(photos_router)

@app.get("/")
def root():
    return {"ok": True}

@app.get("/health/db")
def health_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"db": "ok"}
