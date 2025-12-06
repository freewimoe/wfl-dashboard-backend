"""Pydantic schemas for events."""

from datetime import datetime

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    """Shared event fields."""

    title: str = Field(..., max_length=255)
    description: str | None = None
    start: datetime
    end: datetime
    room_id: int
    is_public: bool = False
    project_id: int | None = None


class EventCreate(EventBase):
    """Payload to create an event."""

    created_by: int | None = None


class EventUpdate(BaseModel):
    """Fields that can be updated on an event."""

    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    start: datetime | None = None
    end: datetime | None = None
    room_id: int | None = None
    is_public: bool | None = None
    project_id: int | None = None


class EventRead(EventBase):
    """Event representation returned by the API."""

    id: int
    created_by: int

    model_config = {"from_attributes": True}
