"""Status endpoints, including dashboard summary aggregation."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.models.event import Event
from app.db.models.news import News
from app.db.models.project import Project
from app.db.session import get_db
from app.schemas.summary import EventSummary, NewsSummary, ProjectSummary, StatusSummary


router = APIRouter(prefix="/status", tags=["status"])


@router.get("/health", summary="Service health check")
def get_health() -> dict[str, str]:
	"""Return basic service health information."""

	return {"status": "online", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/summary", response_model=StatusSummary, summary="Dashboard overview")
def get_summary(db: Session = Depends(get_db)) -> StatusSummary:
	"""Aggregate projects, events, and news for dashboard start view."""

	now = datetime.now(timezone.utc)
	projects = (
		db.query(Project)
		.order_by(Project.created_at.desc())
		.limit(10)
		.all()
	)
	upcoming_events = (
		db.query(Event)
		.filter(Event.start >= now)
		.order_by(Event.start.asc())
		.limit(5)
		.all()
	)
	recent_news = (
		db.query(News)
		.order_by(News.created_at.desc())
		.limit(5)
		.all()
	)

	return StatusSummary(
		projects=[
			ProjectSummary(
				id=project.id,
				title=project.title,
				status=project.status,
				responsible_user_id=project.responsible_user_id,
			)
			for project in projects
		],
		upcoming_events=[
			EventSummary(
				id=event.id,
				title=event.title,
				start=event.start,
				end=event.end,
				room_id=event.room_id,
			)
			for event in upcoming_events
		],
		recent_news=[
			NewsSummary(
				id=news.id,
				title=news.title,
				created_at=news.created_at,
				tags=news.tags,
			)
			for news in recent_news
		],
	)
