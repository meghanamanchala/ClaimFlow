import os

import pytest
from fastapi.testclient import TestClient

# Ensure database module initializes with a test SQLite URL before app import.
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_claimflow.db")

from database import Base, SessionLocal, engine  # noqa: E402
from dependencies import get_db as dependency_get_db  # noqa: E402
from main import app, get_db as main_get_db  # noqa: E402


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def override_db_dependencies():
    def _override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[main_get_db] = _override_get_db
    app.dependency_overrides[dependency_get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


