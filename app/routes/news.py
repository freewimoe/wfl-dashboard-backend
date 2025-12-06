"""REST endpoints for managing news entries."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies import require_roles
from app.db.models.news import News
from app.db.session import get_db
from app.schemas.news import NewsCreate, NewsRead, NewsUpdate

NOT_FOUND_MESSAGE = "News item not found"


router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=list[NewsRead], summary="List news items")
def list_news(
	*,
	db: Session = Depends(get_db),
	tag: str | None = Query(default=None, description="Filter by tag"),
	is_public: bool | None = Query(default=None, description="Restrict to public/private"),
	since: datetime | None = Query(default=None, description="Return entries created after timestamp"),
	limit: int | None = Query(default=None, ge=1, le=100, description="Maximum number of entries"),
) -> list[NewsRead]:
	"""Return news entries filtered by optional criteria."""

	query = db.query(News)
	if is_public is not None:
		query = query.filter(News.is_public == is_public)
	if since is not None:
		query = query.filter(News.created_at >= since)

	news_entries = query.order_by(News.created_at.desc()).all()
	if tag:
		news_entries = [item for item in news_entries if item.tags and tag in item.tags]
	if limit is not None:
		news_entries = news_entries[:limit]
	return [NewsRead.model_validate(item) for item in news_entries]


@router.get("/{news_id}", response_model=NewsRead, summary="Retrieve single news entry")
def get_news(news_id: int, db: Session = Depends(get_db)) -> NewsRead:
	"""Fetch a single news entry by identifier."""

	news_entry = db.get(News, news_id)
	if news_entry is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MESSAGE)
	return NewsRead.model_validate(news_entry)


@router.post("", response_model=NewsRead, status_code=status.HTTP_201_CREATED, summary="Create news entry")
def create_news(
	payload: NewsCreate,
	db: Session = Depends(get_db),
	current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> NewsRead:
	"""Persist a new news entry."""

	author_id = payload.author_id or current_user.id
	news_entry = News(
		title=payload.title,
		body=payload.body,
		tags=payload.tags,
		is_public=payload.is_public,
		project_id=payload.project_id,
		author_id=author_id,
	)
	db.add(news_entry)
	db.commit()
	db.refresh(news_entry)
	return NewsRead.model_validate(news_entry)


@router.put("/{news_id}", response_model=NewsRead, summary="Update news entry")
def update_news(
	news_id: int,
	payload: NewsUpdate,
	db: Session = Depends(get_db),
	current_user=Depends(require_roles("admin", "vorstand", "team")),
) -> NewsRead:
	"""Update news entry content."""

	news_entry = db.get(News, news_id)
	if news_entry is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MESSAGE)

	for field, value in payload.model_dump(exclude_unset=True).items():
		setattr(news_entry, field, value)
	db.add(news_entry)
	db.commit()
	db.refresh(news_entry)
	return NewsRead.model_validate(news_entry)


@router.delete("/{news_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete news entry")
def delete_news(
	news_id: int,
	db: Session = Depends(get_db),
	current_user=Depends(require_roles("admin", "vorstand")),
) -> None:
	"""Remove a news entry permanently."""

	news_entry = db.get(News, news_id)
	if news_entry is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MESSAGE)
	db.delete(news_entry)
	db.commit()
