"""Project management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import require_roles
from app.db.models.project import Project
from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

PROJECT_NOT_FOUND = "Project not found"

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectRead], summary="List projects")
def list_projects(
    *,
    db: Session = Depends(get_db),
    status_filter: str | None = Query(default=None, alias="status"),
) -> list[ProjectRead]:
    """Return all projects, optionally filtered by status."""

    query = db.query(Project)
    if status_filter:
        query = query.filter(Project.status == status_filter)
    projects = query.order_by(Project.created_at.desc()).all()
    return [ProjectRead.model_validate(project) for project in projects]


@router.get("/{project_id}", response_model=ProjectRead, summary="Get project by id")
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    """Return a single project."""

    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    return ProjectRead.model_validate(project)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, summary="Create project")
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> ProjectRead:
    """Create a new project entry."""

    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.put("/{project_id}", response_model=ProjectRead, summary="Update project")
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> ProjectRead:
    """Update a project."""

    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete project")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> None:
    """Delete a project."""

    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=PROJECT_NOT_FOUND)
    db.delete(project)
    db.commit()
