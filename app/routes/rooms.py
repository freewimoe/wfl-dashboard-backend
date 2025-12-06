"""Room management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import require_roles
from app.db.models.room import Room
from app.db.session import get_db
from app.schemas.room import RoomCreate, RoomRead, RoomUpdate

ROOM_NOT_FOUND = "Room not found"

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomRead], summary="List rooms")
def list_rooms(db: Session = Depends(get_db)) -> list[RoomRead]:
    """Return all rooms."""

    rooms = db.query(Room).order_by(Room.name.asc()).all()
    return [RoomRead.model_validate(room) for room in rooms]


@router.post("", response_model=RoomRead, status_code=status.HTTP_201_CREATED, summary="Create room")
def create_room(
    payload: RoomCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> RoomRead:
    """Create a new room record."""

    room = Room(**payload.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return RoomRead.model_validate(room)


@router.put("/{room_id}", response_model=RoomRead, summary="Update room")
def update_room(
    room_id: int,
    payload: RoomUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> RoomRead:
    """Update an existing room."""

    room = db.get(Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_NOT_FOUND)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(room, field, value)
    db.add(room)
    db.commit()
    db.refresh(room)
    return RoomRead.model_validate(room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete room")
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
) -> None:
    """Delete a room."""

    room = db.get(Room, room_id)
    if room is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ROOM_NOT_FOUND)
    db.delete(room)
    db.commit()
