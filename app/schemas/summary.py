"""Schemas for dashboard summary endpoints."""

from datetime import datetime

from pydantic import BaseModel


class ProjectSummary(BaseModel):
    id: int
    title: str
    status: str
    responsible_user_id: int | None = None


class NewsSummary(BaseModel):
    id: int
    title: str
    created_at: datetime | None = None
    tags: list[str] | None = None


class EventSummary(BaseModel):
    id: int
    title: str
    start: datetime
    end: datetime
    room_id: int


class StatusSummary(BaseModel):
    projects: list[ProjectSummary]
    upcoming_events: list[EventSummary]
    recent_news: list[NewsSummary]
