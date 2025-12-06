"""Event management endpoints."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import require_roles
from app.db.models.event import Event
from app.db.session import get_db
from app.schemas.event import EventCreate, EventRead, EventUpdate

EVENT_NOT_FOUND = "Event not found"

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventRead], summary="List events")
def list_events(
    *,
    db: Session = Depends(get_db),
    start_from: datetime | None = Query(default=None, description="Filter events starting after timestamp"),
    start_to: datetime | None = Query(default=None, description="Filter events starting before timestamp"),
    room_id: int | None = Query(default=None, description="Filter by room"),
) -> list[EventRead]:
    """Return events matching the provided filters."""

    query = db.query(Event)
    if start_from:
        query = query.filter(Event.start >= start_from)
    if start_to:
        query = query.filter(Event.start <= start_to)
    if room_id:
        query = query.filter(Event.room_id == room_id)
    events = query.order_by(Event.start.asc()).all()
    return [EventRead.model_validate(event) for event in events]


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED, summary="Create event")
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> EventRead:
    """Create a new event."""

    data = payload.model_dump(exclude_unset=True)
    data["created_by"] = payload.created_by or current_user.id
    event = Event(**data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return EventRead.model_validate(event)


@router.put("/{event_id}", response_model=EventRead, summary="Update event")
def update_event(
    event_id: int,
    payload: EventUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> EventRead:
    """Update event details."""

    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EVENT_NOT_FOUND)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.add(event)
    db.commit()
    db.refresh(event)
    return EventRead.model_validate(event)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete event")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> None:
    """Delete an event."""

    event = db.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=EVENT_NOT_FOUND)
    db.delete(event)
    db.commit()
