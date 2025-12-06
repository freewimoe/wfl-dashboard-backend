"""Task management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, require_roles
from app.db.models.task import Task
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

TASK_NOT_FOUND = "Task not found"

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead], summary="List tasks")
def list_tasks(
    *,
    db: Session = Depends(get_db),
    assignee_id: int | None = Query(default=None, description="Filter tasks by assignee"),
    project_id: int | None = Query(default=None, description="Filter tasks by project"),
    status_filter: str | None = Query(default=None, alias="status"),
) -> list[TaskRead]:
    """Return tasks matching the provided filters."""

    query = db.query(Task)
    if assignee_id is not None:
        query = query.filter(Task.assignee_id == assignee_id)
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)
    if status_filter is not None:
        query = query.filter(Task.status == status_filter)
    tasks = query.order_by(Task.due_date.asc(), Task.created_at.desc()).all()
    return [TaskRead.model_validate(task) for task in tasks]


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED, summary="Create task")
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> TaskRead:
    """Create a task for the organisation."""

    data = payload.model_dump(exclude_unset=True)
    data["created_by"] = payload.created_by or current_user.id
    task = Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead, summary="Update task")
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> TaskRead:
    """Update task fields; permissions enforced by role."""

    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND)

    if current_user.role not in {"admin", "vorstand", "team"} and task.assignee_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify this task")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> None:
    """Delete a task."""

    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=TASK_NOT_FOUND)
    db.delete(task)
    db.commit()
