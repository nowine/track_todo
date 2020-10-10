from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UnicodeText, Sequence
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, Sequence('projects_id_seq'), primary_key=True, index=True)
    name = Column(String(50), index=True)

    items = relationship("Item", back_populates="project")