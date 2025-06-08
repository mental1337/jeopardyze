import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add the parent directory (backend) to Python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)

# Now we can import app modules
from app.models.base import Base
from app.models import User, QuizBoard, Category, Question, GameSession, QuestionAttempt
from app.main import app
from app.core.database import get_db

# Create a test database engine using SQLite in-memory database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Creates a fresh database for each test.
    The database is created in memory and is dropped after the test.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new database session for the test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a new FastAPI TestClient that uses the `db` fixture to override
    the `get_db` dependency.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # Clear the dependency override
        app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_send_email():
    """
    Fixture to mock the send_email function and print email details.
    This fixture is automatically applied to all tests in the directory.
    """
    with patch('app.services.email_verify_service.send_email') as mock:
        def side_effect(to_email, subject, html_content):
            print(f"Mock sending email to: {to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {html_content}")
            return True
        mock.side_effect = side_effect
        yield mock


### FYI: ###

"""
The above fixtures can be used in test functions like this:

```
def test_login_success(client: TestClient, db: Session):
    # Use db session to create test data
    user = User(...)
    db.add(user)
    db.commit()
    
    # Use client to make requests
    response = client.post("/api/auth/login", json=login_data)
```

The database will be automatically:
1. Created before each test
2. Provided to the test function
3. Cleaned up after the test completes

"""
