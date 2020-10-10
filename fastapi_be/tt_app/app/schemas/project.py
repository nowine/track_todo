from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


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