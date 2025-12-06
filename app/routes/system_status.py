"""Endpoints to manage external system status information."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import require_roles
from app.db.models.system_status import SystemStatus
from app.db.session import get_db
from app.schemas.system_status import SystemStatusCreate, SystemStatusRead, SystemStatusUpdate

STATUS_NOT_FOUND = "System status entry not found"

router = APIRouter(prefix="/system/status", tags=["system-status"])


@router.get("", response_model=list[SystemStatusRead], summary="List system statuses")
def list_system_statuses(db: Session = Depends(get_db)) -> list[SystemStatusRead]:
    """Return all known system status records."""

    entries = db.query(SystemStatus).order_by(SystemStatus.service.asc()).all()
    return [SystemStatusRead.model_validate(entry) for entry in entries]


@router.post("", response_model=SystemStatusRead, status_code=status.HTTP_201_CREATED, summary="Create system status")
def create_system_status(
    payload: SystemStatusCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> SystemStatusRead:
    """Create a new system status entry."""

    entry = SystemStatus(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return SystemStatusRead.model_validate(entry)


@router.patch("/{entry_id}", response_model=SystemStatusRead, summary="Update system status")
def update_system_status(
    entry_id: int,
    payload: SystemStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> SystemStatusRead:
    """Update an existing system status entry."""

    entry = db.get(SystemStatus, entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=STATUS_NOT_FOUND)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return SystemStatusRead.model_validate(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete system status")
def delete_system_status(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> None:
    """Delete a system status entry."""

    entry = db.get(SystemStatus, entry_id)
    if entry is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=STATUS_NOT_FOUND)
    db.delete(entry)
    db.commit()
