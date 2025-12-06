"""SQLAlchemy model for scheduled events."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Event(Base):
    """Calendar entry associated with rooms and projects."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    room = relationship("Room", back_populates="events")
    project = relationship("Project", back_populates="events")
    creator = relationship("User", back_populates="events_created")
