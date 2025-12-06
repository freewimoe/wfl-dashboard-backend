"""FastAPI application entrypoint for the WfL dashboard backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import register_routes


def create_app() -> FastAPI:
	"""Create and configure the FastAPI instance."""

	app = FastAPI(title="WfL Dashboard API", version="1.0.0")

	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	register_routes(app)

	return app


app = create_app()


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
