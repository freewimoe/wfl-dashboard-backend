"""Pydantic schemas for rooms."""

from pydantic import BaseModel, Field


class RoomBase(BaseModel):
    """Shared room fields."""

    name: str = Field(..., max_length=255)
    description: str | None = None
    capacity: int | None = None


class RoomCreate(RoomBase):
    """Payload to create a room."""


class RoomUpdate(BaseModel):
    """Fields that can be updated on a room."""

    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    capacity: int | None = None


class RoomRead(RoomBase):
    """Room representation returned by the API."""

    id: int

    model_config = {"from_attributes": True}
