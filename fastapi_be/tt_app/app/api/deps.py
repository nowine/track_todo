from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.db.database import SessionLocal
from app import models, crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    user_id: str = 0
    ) -> models.User:
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
