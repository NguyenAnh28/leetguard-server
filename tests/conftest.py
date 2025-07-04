"""
Pytest configuration and common fixtures for LeetGuard tests.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import app
from app.db.session import get_db
from app.models.user import Base
from app.config import settings

# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine

@pytest.fixture(scope="session")
def test_db(test_engine):
    """Create test database tables."""
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(test_db):
    """Create a new database session for each test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def test_verification_data():
    """Sample verification data for testing."""
    return {
        "email": "test@example.com",
        "code": "123456"
    }

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("REFRESH_SECRET_KEY", "test-refresh-secret-key")
    monkeypatch.setenv("RESEND_API_KEY", "test-resend-api-key")
    monkeypatch.setenv("FROM_EMAIL", "test@example.com")
    monkeypatch.setenv("FRONTEND_URL", "https://test.com")
    monkeypatch.setenv("DATABASE_URL", TEST_DATABASE_URL) 