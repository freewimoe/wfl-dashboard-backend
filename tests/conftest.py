"""Shared pytest fixtures for API tests."""

import os
import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import bcrypt

ADMIN_PASSWORD = "AdminPass_123!"

# Ensure project root is importable when running tests directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import get_settings
from app.core.security import get_password_hash
from app.db import session as db_session
from app.db.base import Base
from app.db.models import User
from app.main import create_app


@pytest.fixture(scope="session")
def test_engine(tmp_path_factory: pytest.TempPathFactory):
    """Create a dedicated SQLite database for tests."""

    db_file = tmp_path_factory.mktemp("data") / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    os.environ.setdefault("SECRET_KEY", "test-secret-key")
    get_settings.cache_clear()  # refresh settings after env overrides

    engine = create_engine(
        os.environ["DATABASE_URL"], connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    # Wire test engine into application session module
    db_session.SessionLocal = TestingSessionLocal
    db_session.engine = engine

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session_fixture(test_engine) -> Generator:
    """Provide a transactional database session for each test."""

    TestingSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="session")
def client(test_engine) -> Generator[TestClient, None, None]:
    """FastAPI test client connected to the temporary database."""

    app = create_app()

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def admin_credentials(client, test_engine) -> dict[str, str]:
    """Create and return credentials for an admin user."""

    SessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)
    session = SessionLocal()
    try:
        admin = User(
            name="Admin",
            email="admin@example.com",
            password_hash=bcrypt.hashpw(ADMIN_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
            role="admin",
        )
        session.add(admin)
        session.commit()
    finally:
        session.close()

    return {"email": "admin@example.com", "password": ADMIN_PASSWORD}
