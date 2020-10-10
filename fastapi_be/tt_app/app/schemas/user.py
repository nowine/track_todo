from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


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