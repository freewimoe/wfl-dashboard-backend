"""SQLAlchemy model describing rooms in the venue."""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Room(Base):
    """Physical room that can host events."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    capacity = Column(Integer)

    events = relationship("Event", back_populates="room")
