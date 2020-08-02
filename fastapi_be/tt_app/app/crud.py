from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from typing import Optional

from . import models, schemas

def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(
        subject=item.subject,
        target_completion=item.target_completion,
        effort_unit = item.effort_unit,
        effort_count = item.effort_count,
        detail = item.detail,
        owner_id = item.owner_id,
        creator_id = item.creator_id,
        last_updater_id = item.creator_id,
        parent_id = item.parent_id,
        project_id = item.project_id,
        status = item.status if item.status else 'NEW'
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item_by_id(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id==item_id).first()


def get_items(db:Session, skip: int = 0, limit: int = 100): 
    return db.query(models.Item).offset(skip).limit(limit).all()

"""
def update_item(db: Session, item: schemas.ItemUpdate) -> models.Item:
    db_item = db.query(models.Item).filter(models.Item.id=item.id).first()
    if db_item: 
        db_item.subject = item.subject #if item.subject else db_item.subject
        db_item.owner_id = item.owner_id #if item.owner_id else db_item.owner_id
        #creator id should not be changed. 
        db_item.target_completion = item.target_completion #if item.target_completion else db_item.target_completion
"""

def update_item(db: Session, db_item: models.Item, data_item: schemas.ItemUpdate) -> models.Item:
    db_data = jsonable_encoder(db_item)
    update_date = data_item.dict(exclude_unset=True)
    for field in db_data:
        if field in update_date:
            setattr(db_item, field, update_date[field])
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, id: int) -> models.Item:
    obj = db.query(models.Item).get(id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj