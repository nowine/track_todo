from sqlalchemy.orm import Session
from typing import List, Any

from .base import CRUDBase
from app.models import Item
from app.schemas import ItemCreate, ItemUpdate

class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def create(self, db: Session, *, obj_in: ItemCreate) -> Item:
        '''
        Need to overwrite the create method to specify the last update id to the creator id if it is not provided
        '''
        if not hasattr(obj_in, 'last_updater_id') or getattr(obj_in, 'last_updater_id') is None:
            setattr(obj_in, 'last_updater_id', getattr(obj_in, 'creator_id'))
        return super().create(db=db, obj_in=obj_in)

    def get_by_owner(self, db: Session, *, owner_id: int, skip:int=0, limit: int = 100) -> List[Any]: 
        # No validate of the user existence and authority as it suppose be validated before 
        return db.query(self.model).filter(Item.owner_id == owner_id).offset(skip).limit(limit).all()

item = CRUDItem(Item)