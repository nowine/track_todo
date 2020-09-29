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
    
class ItemDeleted(ItemUpdate):
    '''
    Added this deleted schema because the deleted item will be detached from the session, so could no more use
    the relationship to get the owner/creator/project/parent/children information into response. 

    This is a tactical solution, and this could already help to re-create objects.

    TO-DO: Find the solution to use the session. 
    '''
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class Item(ItemBase):
    id: int
    last_updater_id: int
    created_at: datetime
    last_updated_by: datetime
    owner: User
    creator: User
    last_updater: User
    # Self-referring Type annotation, use the string for replacement first.
    children: List['Item'] = []
    parent: 'Item' = None
    project: Optional[Project] = None
    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

# And after defining the "Item" schema, use the below function to "replace" the 
# string value `Item` with the real Class
Item.update_forward_refs()