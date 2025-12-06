"""SQLAlchemy model for simple key-value metrics."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db.base import Base


class Metric(Base):
    """Dashboard metric aggregated from various systems."""

    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    value = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
