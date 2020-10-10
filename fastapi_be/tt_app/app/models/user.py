from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UnicodeText, Sequence
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('users_id_seq'), primary_key=True, index=True)
    nickname = Column(String(50), index=True)

    #own_items = relationship("Item", back_populates="owner")
    #create_items = relationship("Item", back_populates="creator")