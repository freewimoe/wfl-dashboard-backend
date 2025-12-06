"""Declarative base and model imports."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# Import models here so Alembic and SQLAlchemy know about them
from app.db.models import user, project, news, room, event, task, metric, system_status  # noqa: E402,F401
