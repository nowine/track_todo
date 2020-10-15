from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps

from app import models, schemas, crud

route = APIRouter()

@route.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(deps.get_db)) -> models.User:
    return crud.user.create(obj_in=user, db=db)

@route.get('/{user_id}', response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(deps.get_db)) -> models.user:
    user =  crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user