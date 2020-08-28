from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

from . import models


class UserBase(BaseModel):
    nickname: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class User(UserBase):
    id: int

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    id: int


class Project(ProjectBase):
    id: int

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class ItemBase(BaseModel):
    subject: str
    target_completion: Optional[datetime] = None
    effort_unit: Optional[str] = None
    effort_count: Optional[int] = None
    detail: Optional[str] = None
    owner_id: int
    creator_id: int
    parent_id: Optional[int] = None
    project_id: Optional[int] = None
    status: str


class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    id: int 
    last_updater_id: int


class Item(ItemBase):
    id: int
    last_updater_id: int
    created_at: datetime
    last_updated_by: datetime
    owner: models.User
    creator: models.User
    last_updater: models.User
    children: List[models.Item] = []
    parent: models.Item
    project: models.Project

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
