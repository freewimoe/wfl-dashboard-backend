"""Auth-related Pydantic schemas."""

from pydantic import BaseModel


class Token(BaseModel):
    """JWT response body."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Payload expected inside JWTs."""

    sub: str
    exp: int


class LoginRequest(BaseModel):
    """Login payload using username and password."""

    email: str
    password: str
