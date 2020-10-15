from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, UnicodeText, Sequence
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from app.db.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Sequence('items_id_seq'), primary_key=True, index=True)
    subject = Column(String(150), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    target_completion = Column(DateTime, nullable=True)
    effort_unit = Column(String(3))
    effort_count = Column(Integer)
    status = Column(String(3))
    parent_id = Column(Integer, ForeignKey('items.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    detail = Column(UnicodeText)
    last_updater_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    last_updated_by = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    #owner = relationship("User", back_populates="own_items", foreign_keys=[owner_id])
    #creator = relationship("User", back_populates="create_items", foreign_keys=[creator_id])
    owner = relationship("User", foreign_keys=[owner_id], backref='own_items')
    creator = relationship("User", foreign_keys=[creator_id], backref='create_items')
    last_updater = relationship("User", foreign_keys=[last_updater_id])
    children = relationship("Item", backref=backref('parent', remote_side=[id]))
    project = relationship("Project", back_populates="items")