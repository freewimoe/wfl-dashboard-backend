"""Pydantic schemas for user operations."""

from datetime import datetime

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Fields shared across user representations."""

    name: str = Field(..., max_length=255)
    email: str
    role: str


class UserCreate(UserBase):
    """Payload required to create a user."""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Editable user fields."""

    name: str | None = Field(default=None, max_length=255)
    role: str | None = None


class UserPasswordUpdate(BaseModel):
    """Payload to update a user's password."""

    password: str = Field(..., min_length=12)


class UserRead(UserBase):
    """User representation returned by the API."""

    id: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
