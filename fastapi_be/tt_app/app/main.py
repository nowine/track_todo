from typing import List, Dict, Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schemas, models
from app.db.database import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session=Depends(get_db)):
    return crud.item.create(db=db, obj_in=item)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session=Depends(get_db)):
    db_item = crud.item.get(db=db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=dict())
def delete_item(item_id: int, db: Session=Depends(get_db)):
    db_item = crud.item.remove(db=db, id=item_id)
    #print(db_item)
    #db_item = crud.get_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    #crud.delete_item(db, item_id)
    return db_item