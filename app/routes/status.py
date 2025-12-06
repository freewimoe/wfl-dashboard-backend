"""Status endpoints for service health monitoring."""

from fastapi import APIRouter


router = APIRouter(prefix="", tags=["status"])


@router.get("/status", summary="Service health check")
async def get_status() -> dict[str, str]:
	"""Return basic service health information."""

	return {"status": "online", "version": "1.0.0"}
