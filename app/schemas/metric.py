"""Pydantic schemas for dashboard metrics."""

from datetime import datetime

from pydantic import BaseModel


class MetricBase(BaseModel):
    """Shared metric fields."""

    name: str
    value: float


class MetricCreate(MetricBase):
    """Payload to create a metric entry."""


class MetricUpdate(BaseModel):
    """Mutable fields for a metric."""

    value: float | None = None


class MetricRead(MetricBase):
    """Metric representation returned by the API."""

    id: int
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}
