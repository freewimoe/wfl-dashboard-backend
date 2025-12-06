"""Metric management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import require_roles
from app.db.models.metric import Metric
from app.db.session import get_db
from app.schemas.metric import MetricCreate, MetricRead, MetricUpdate

METRIC_NOT_FOUND = "Metric not found"

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("", response_model=list[MetricRead], summary="List metrics")
def list_metrics(db: Session = Depends(get_db)) -> list[MetricRead]:
    """Return all metrics."""

    metrics = db.query(Metric).order_by(Metric.name.asc()).all()
    return [MetricRead.model_validate(metric) for metric in metrics]


@router.post("", response_model=MetricRead, status_code=status.HTTP_201_CREATED, summary="Create metric")
def create_metric(
    payload: MetricCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> MetricRead:
    """Create or overwrite a metric entry."""

    metric = Metric(**payload.model_dump())
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return MetricRead.model_validate(metric)


@router.patch("/{metric_id}", response_model=MetricRead, summary="Update metric")
def update_metric(
    metric_id: int,
    payload: MetricUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> MetricRead:
    """Update metric values."""

    metric = db.get(Metric, metric_id)
    if metric is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=METRIC_NOT_FOUND)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(metric, field, value)
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return MetricRead.model_validate(metric)


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete metric")
def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "vorstand")),
) -> None:
    """Delete a metric entry."""

    metric = db.get(Metric, metric_id)
    if metric is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=METRIC_NOT_FOUND)
    db.delete(metric)
    db.commit()
