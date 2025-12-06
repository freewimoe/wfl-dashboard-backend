"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.dependencies import get_current_user, require_roles
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import UserRead, UserUpdate, UserPasswordUpdate

USER_NOT_FOUND = "User not found"
PERMISSION_DENIED = "Insufficient permissions"

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead], summary="List users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "vorstand")),
) -> list[UserRead]:
    """Return all users ordered by creation time."""

    users = db.query(User).order_by(User.created_at.asc()).all()
    return [UserRead.model_validate(user) for user in users]


@router.get("/me", response_model=UserRead, summary="Retrieve current user")
def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """Return the authenticated user's information."""

    return UserRead.model_validate(current_user)


@router.get("/{user_id}", response_model=UserRead, summary="Get user by id")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Return a user if permitted."""

    if current_user.role not in {"admin", "vorstand"} and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=PERMISSION_DENIED)

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)

    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead, summary="Update user profile")
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Update user details respecting role constraints."""

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)

    is_self = current_user.id == user_id
    is_admin = current_user.role == "admin"

    if not is_self and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=PERMISSION_DENIED)

    update_data = payload.model_dump(exclude_unset=True)
    if "role" in update_data and not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins may change roles")

    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


@router.patch(
    "/{user_id}/password",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Update user password",
)
def update_password(
    user_id: int,
    payload: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Update a user's password; allowed for admins or the user themselves."""

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)

    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=PERMISSION_DENIED)

    user.password_hash = get_password_hash(payload.password)
    db.add(user)
    db.commit()


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete user")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin")),
) -> None:
    """Remove a user from the system."""

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
    db.delete(user)
    db.commit()
