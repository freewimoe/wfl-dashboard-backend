"""News endpoints exposed to consumers of the dashboard API."""

from fastapi import APIRouter

from app.models.news import NewsItem
from app.services.news_service import list_news


router = APIRouter(prefix="/news", tags=["news"])


@router.get("", response_model=list[NewsItem], summary="List news items")
async def get_news() -> list[NewsItem]:
	"""Return news entries for the dashboard."""

	return list_news()
