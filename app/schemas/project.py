"""Pydantic schemas for project resources."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.summary import EventSummary, NewsSummary


class ProjectBase(BaseModel):
    """Shared project fields."""

    title: str = Field(..., max_length=255)
    description: str | None = None
    status: str = Field(default="green")
    responsible_user_id: int | None = None


class ProjectCreate(ProjectBase):
    """Payload for creating a project."""


class ProjectUpdate(BaseModel):
    """Fields that may be updated on a project."""

    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    status: str | None = None
    responsible_user_id: int | None = None


class ProjectRead(ProjectBase):
    """Project representation returned by the API."""

    id: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class ProjectSummaryStats(BaseModel):
    """Aggregated details for a single project dashboard view."""

    project: ProjectRead
    total_tasks: int
    task_counts: dict[str, int]
    upcoming_events: list[EventSummary]
    recent_news: list[NewsSummary]
