"""SQLAlchemy model for tasks assigned to team members."""

from datetime import datetime

from sqlalchemy import CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Task(Base):
    """Tasks that track operational work in the organisation."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, nullable=False, default="open")
    due_date = Column(Date)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks_assigned", foreign_keys=[assignee_id])
    creator = relationship("User", back_populates="tasks_created", foreign_keys=[created_by])

    __table_args__ = (
        CheckConstraint("status IN ('open','in_progress','done')", name="ck_tasks_status"),
    )
