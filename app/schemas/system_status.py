"""Pydantic schemas for service status entries."""

from datetime import datetime

from pydantic import BaseModel


class SystemStatusBase(BaseModel):
    """Shared system status fields."""

    service: str
    status: str = "ok"
    message: str | None = None


class SystemStatusCreate(SystemStatusBase):
    """Payload to create a system status entry."""


class SystemStatusUpdate(BaseModel):
    """Mutable fields for service status updates."""

    status: str | None = None
    message: str | None = None


class SystemStatusRead(SystemStatusBase):
    """System status representation returned by the API."""

    id: int
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
