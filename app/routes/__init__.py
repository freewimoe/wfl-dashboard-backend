"""Route registration helpers for the FastAPI app."""

from fastapi import APIRouter, FastAPI

from app.routes import auth, events, metrics, news, projects, rooms, status, system_status, tasks, users

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(status.router)
api_router.include_router(projects.router)
api_router.include_router(news.router)
api_router.include_router(events.router)
api_router.include_router(rooms.router)
api_router.include_router(tasks.router)
api_router.include_router(metrics.router)
api_router.include_router(system_status.router)
api_router.include_router(users.router)


def register_routes(app: FastAPI) -> None:
    """Attach all API routers to the given app."""

    app.include_router(api_router)


__all__ = ["register_routes"]
