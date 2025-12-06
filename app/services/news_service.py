"""Domain services for news retrieval and persistence."""

from datetime import date

from app.models.news import NewsItem


def list_news() -> list[NewsItem]:
	"""Return placeholder news items until a database is connected."""

	return [
		NewsItem(id=1, title="Willkommen beim WfL-Dashboard", timestamp=date(2025, 12, 1)),
		NewsItem(id=2, title="Nextcloud integriert", timestamp=date(2025, 12, 2)),
	]
