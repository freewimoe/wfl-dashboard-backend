"""Pydantic models for news domain objects."""

from datetime import date

from pydantic import BaseModel


class NewsItem(BaseModel):
	"""Textual update shown on the dashboard."""

	id: int
	title: str
	timestamp: date
