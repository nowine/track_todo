from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session=Depends(deps.get_db)):
    return crud.item.create(db=db, obj_in=item)

@router.get("/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session=Depends(deps.get_db)):
    db_item = crud.item.get(db=db, id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.get("/", response_model=List[schemas.Item])
def read_itmes(
    db:Session = Depends(deps.get_db), 
    skip: int = 0, 
    limit: int = 100,
    user: models.User = Depends(deps.get_current_user) 
    ) -> Any:
    return crud.item.get_by_owner(db, owner_id=user.id, skip=skip, limit=limit)

@router.delete("/{item_id}", response_model=dict())
def delete_item(item_id: int, db: Session=Depends(deps.get_db)):
    db_item = crud.item.remove(db=db, id=item_id)
    #print(db_item)
    #db_item = crud.get_item_by_id(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    #crud.delete_item(db, item_id)
    return db_item