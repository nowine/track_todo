from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas, models
from .database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session=Depends(get_db)):
    return crud.create_item(db, item)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(user_id: int, db: Session=Depends(get_db)):
    db_item = crud.get_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item