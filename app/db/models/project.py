"""SQLAlchemy model for organisational projects."""

from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Project(Base):
    """Project or workstream tracked in the dashboard."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, nullable=False, default="green")
    responsible_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    responsible_user = relationship("User", back_populates="projects_responsible")
    news_entries = relationship("News", back_populates="project")
    events = relationship("Event", back_populates="project")
    tasks = relationship("Task", back_populates="project")

    __table_args__ = (
        CheckConstraint("status IN ('green','yellow','red')", name="ck_projects_status"),
    )
