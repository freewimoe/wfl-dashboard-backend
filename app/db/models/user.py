"""SQLAlchemy model for users handling authentication and roles."""

from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    """Application user with role membership."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects_responsible = relationship("Project", back_populates="responsible_user")
    news_entries = relationship("News", back_populates="author")
    events_created = relationship("Event", back_populates="creator")
    tasks_assigned = relationship("Task", back_populates="assignee", foreign_keys="Task.assignee_id")
    tasks_created = relationship("Task", back_populates="creator", foreign_keys="Task.created_by")

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin','vorstand','team','mitarbeit','public')",
            name="ck_users_role",
        ),
    )
