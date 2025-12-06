"""Route registration helpers for the FastAPI app."""

from fastapi import FastAPI

from app.routes import news, status


def register_routes(app: FastAPI) -> None:
	"""Attach all API routers to the given app."""

	app.include_router(status.router)
	app.include_router(news.router)

__all__ = ["register_routes"]
