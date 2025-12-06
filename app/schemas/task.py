"""Pydantic schemas for tasks."""

from datetime import date, datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Shared task fields."""

    title: str = Field(..., max_length=255)
    description: str | None = None
    project_id: int | None = None
    assignee_id: int | None = None
    status: str = Field(default="open")
    due_date: date | None = None


class TaskCreate(TaskBase):
    """Payload to create a task."""

    created_by: int | None = None


class TaskUpdate(BaseModel):
    """Mutable fields for a task."""

    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    project_id: int | None = None
    assignee_id: int | None = None
    status: str | None = None
    due_date: date | None = None


class TaskRead(TaskBase):
    """Task representation returned by the API."""

    id: int
    created_by: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
