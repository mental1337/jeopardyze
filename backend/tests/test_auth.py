import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth_service import get_password_hash
from app.services.email_verify_service import send_verification_email

@pytest.fixture
def test_user(db: Session) -> User:
    """
    Fixture to create a test user in the database.
    """
    password = "testpass123"
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash=get_password_hash(password)
    )
    db.add(user)
    db.commit()
    # Attach plain password for use in tests
    setattr(user, "password", password)
    return user

def test_login_success(client: TestClient, test_user: User):
    # Try to login
    login_data = {
        "username_or_email": test_user.username,
        "password": test_user.password
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, test_user: User):
    # Try to login with wrong password
    login_data = {
        "username_or_email": test_user.username,
        "password": "wrongpassword"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username/email or password" in response.json()["detail"]

def test_login_nonexistent_user(client: TestClient):
    login_data = {
        "username_or_email": "nonexistent",
        "password": "password123"
    }
    
    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username/email or password" in response.json()["detail"]

def test_register_success(client: TestClient, db: Session):
    print("Running test_register_success")
    
    # Test data
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "testpass123"
    }
    
    # Make register request
    response = client.post("/api/auth/register", json=user_data)    
    print("Ran client.post")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Verification code sent to email"
    assert data["email"] == user_data["email"]
    
    # Verify user was created in database (unverified)
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert not user.is_verified
    
    # Verify verification code was generated and stored in database
    assert user.verification_code is not None
    assert len(user.verification_code) == 6

def test_register_duplicate_username(client: TestClient, test_user: User):
    # Try to register with same username
    user_data = {
        "username": test_user.username,
        "email": "new@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Username is already registered" in response.json()["detail"]

def test_register_duplicate_email(client: TestClient, test_user: User):
    # Try to register with same email
    user_data = {
        "username": "newuser",
        "email": test_user.email,
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email is already registered" in response.json()["detail"]

def test_verify_email_success(client: TestClient, db: Session):
    # Create an unverified user
    user = User(
        username="verifyuser",
        email="verify@example.com",
        password_hash=get_password_hash("testpass123"),
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    # Generate verification code
    code = send_verification_email(db, user.email)
    
    # Verify email
    verify_data = {
        "email": user.email,
        "code": code
    }
    
    response = client.post("/api/auth/verify-email", json=verify_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Email verified successfully"
    assert data["is_verified"] == True
    assert "access_token" in data
    
    # Verify user is now verified
    db.refresh(user)
    assert user.is_verified
    # Verify code was cleared after successful verification
    assert user.verification_code is None

def test_verify_email_wrong_code(client: TestClient, db: Session):
    # Create an unverified user
    user = User(
        username="wrongcodeuser",
        email="wrongcode@example.com",
        password_hash=get_password_hash("testpass123"),
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    # Generate verification code
    send_verification_email(db, user.email)
    
    # Try to verify with wrong code
    verify_data = {
        "email": user.email,
        "code": "000000"  # Wrong code
    }
    
    response = client.post("/api/auth/verify-email", json=verify_data)
    assert response.status_code == 400
    assert "Invalid verification code" in response.json()["detail"]
    
    # Verify user is still unverified
    db.refresh(user)
    assert not user.is_verified
    # Verify code was not cleared after failed verification
    assert user.verification_code is not None

def test_verify_email_nonexistent_user(client: TestClient):
    verify_data = {
        "email": "nonexistent@example.com",
        "code": "123456"
    }
    
    response = client.post("/api/auth/verify-email", json=verify_data)
    assert response.status_code == 400
    assert "User not found" in response.json()["detail"] 