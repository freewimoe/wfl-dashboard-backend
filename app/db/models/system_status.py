"""SQLAlchemy model storing service health information."""

from datetime import datetime

from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Text

from app.db.base import Base


class SystemStatus(Base):
    """Represents current status of external/internal services."""

    __tablename__ = "system_status"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, default="ok")
    message = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("status IN ('ok','warning','down','planned')", name="ck_system_status_state"),
    )
