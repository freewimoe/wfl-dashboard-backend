"""SQLAlchemy model representing internal news posts."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class News(Base):
    """Short updates published to teams and members."""

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)
    is_public = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="news_entries")
    author = relationship("User", back_populates="news_entries")
