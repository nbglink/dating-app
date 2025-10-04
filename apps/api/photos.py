from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
import os, uuid, pathlib

from db import SessionLocal
from models import Photo, User
from auth import get_current_user   # използваме вече наличния guard от auth.py
from storage import put_object

router = APIRouter(prefix="/photos", tags=["photos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # безопасно име на файл
    ext = pathlib.Path(file.filename or "").suffix.lower()[:10] or ".jpg"
    object_name = f"user-{user.id}/{uuid.uuid4().hex}{ext}"

    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty file")

    # качваме в MinIO
    put_object(object_name, data=iter([data]), length=len(data), content_type=file.content_type)

    # запис в DB
    row = Photo(user_id=user.id, object_key=object_name, content_type=file.content_type)
    db.add(row)
    db.commit()
    db.refresh(row)

    return {"id": row.id, "key": row.object_key, "content_type": row.content_type}

@router.get("/my")
def list_my_photos(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = db.scalars(select(Photo).where(Photo.user_id == user.id).order_by(Photo.id.desc())).all()
    return [{"id": r.id, "key": r.object_key, "content_type": r.content_type, "created_at": r.created_at} for r in rows]
