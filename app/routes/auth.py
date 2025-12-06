"""Authentication endpoints providing JWT handling."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models.user import User
from app.db.session import get_db
from app.dependencies import require_roles
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token, summary="Authenticate user and obtain token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    """Validate credentials and return an access token."""

    user = db.query(User).filter(User.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    settings = get_settings()
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(subject=user.email, expires_delta=access_token_expires)
    return Token(access_token=token)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Create a new user")
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
) -> UserRead:
    """Create a new application user."""

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        role=payload.role,
        password_hash=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)
