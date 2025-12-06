"""FastAPI application entrypoint for the WfL dashboard backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db import base  # noqa: F401 - ensures models are registered
from app.db.session import engine
from app.routes import register_routes


def create_app() -> FastAPI:
	"""Create and configure the FastAPI instance."""

	settings = get_settings()
	app = FastAPI(title=settings.app_name, version="1.0.0")

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	@app.on_event("startup")
	def _on_startup() -> None:
		base.Base.metadata.create_all(bind=engine)

	register_routes(app)

	return app


app = create_app()


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
