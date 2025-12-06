"""Pydantic schemas for news items."""

from datetime import datetime

from pydantic import BaseModel, Field


class NewsBase(BaseModel):
    """Shared fields for news operations."""

    title: str = Field(..., max_length=255)
    body: str
    tags: list[str] | None = None
    is_public: bool = False
    project_id: int | None = None


class NewsCreate(NewsBase):
    """Payload for creating news entries."""

    author_id: int | None = None


class NewsUpdate(BaseModel):
    """Mutable fields for news entries."""

    title: str | None = Field(default=None, max_length=255)
    body: str | None = None
    tags: list[str] | None = None
    is_public: bool | None = None
    project_id: int | None = None


class NewsRead(NewsBase):
    """News representation returned by the API."""

    id: int
    author_id: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
