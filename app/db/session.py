"""Database session and engine configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

_settings = get_settings()
engine = create_engine(
    _settings.database_url,
    connect_args={"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yield a database session that closes after use."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
