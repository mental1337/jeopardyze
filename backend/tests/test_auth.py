import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.services.auth_service import get_password_hash
from app.services.email_service import send_verification_email, verification_codes

client = TestClient(app)

def test_signup_success(db: Session):
    # Test data
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    # Make signup request
    response = client.post("/api/auth/signup", json=user_data)
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify user was created in database
    user = db.query(User).filter(User.username == user_data["username"]).first()
    assert user is not None
    assert user.email == user_data["email"]
    assert user.username == user_data["username"]

def test_signup_duplicate_username(db: Session):
    # Create a user first
    existing_user = User(
        username="existinguser",
        email="existing@example.com",
        password_hash=get_password_hash("password123")
    )
    db.add(existing_user)
    db.commit()
    
    # Try to signup with same username
    user_data = {
        "username": "existinguser",
        "email": "new@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_signup_duplicate_email(db: Session):
    # Create a user first
    existing_user = User(
        username="user1",
        email="existing@example.com",
        password_hash=get_password_hash("password123")
    )
    db.add(existing_user)
    db.commit()
    
    # Try to signup with same email
    user_data = {
        "username": "newuser",
        "email": "existing@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/signup", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success(db: Session):
    # Create a test user
    password = "testpass123"
    user = User(
        username="loginuser",
        email="login@example.com",
        password_hash=get_password_hash(password)
    )
    db.add(user)
    db.commit()
    
    # Try to login
    login_data = {
        "username": "loginuser",
        "password": password
    }
    
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(db: Session):
    # Create a test user
    user = User(
        username="wrongpassuser",
        email="wrongpass@example.com",
        password_hash=get_password_hash("correctpass")
    )
    db.add(user)
    db.commit()
    
    # Try to login with wrong password
    login_data = {
        "username": "wrongpassuser",
        "password": "wrongpass"
    }
    
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_login_nonexistent_user():
    login_data = {
        "username": "nonexistent",
        "password": "password123"
    }
    
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_register_success(db: Session):
    # Clear any existing verification codes
    verification_codes.clear()
    
    # Test data
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "testpass123"
    }
    
    # Make register request
    response = client.post("/api/auth/register", json=user_data)
    
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
    
    # Verify verification code was generated
    assert user_data["email"] in verification_codes

def test_register_duplicate_username(db: Session):
    # Create a user first
    existing_user = User(
        username="existinguser",
        email="existing@example.com",
        password_hash=get_password_hash("password123")
    )
    db.add(existing_user)
    db.commit()
    
    # Try to register with same username
    user_data = {
        "username": "existinguser",
        "email": "new@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Username is already registered" in response.json()["detail"]

def test_register_duplicate_email(db: Session):
    # Create a user first
    existing_user = User(
        username="user1",
        email="existing@example.com",
        password_hash=get_password_hash("password123")
    )
    db.add(existing_user)
    db.commit()
    
    # Try to register with same email
    user_data = {
        "username": "newuser",
        "email": "existing@example.com",
        "password": "testpass123"
    }
    
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email is already registered" in response.json()["detail"]

def test_verify_email_success(db: Session):
    # Clear any existing verification codes
    verification_codes.clear()
    
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
    code = send_verification_email(user.email)
    
    # Verify email
    verify_data = {
        "email": user.email,
        "code": code
    }
    
    response = client.post("/api/auth/verify-email", json=verify_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_id"] == user.id
    assert data["username"] == user.username
    assert data["email"] == user.email
    
    # Verify user is now verified
    db.refresh(user)
    assert user.is_verified

def test_verify_email_wrong_code(db: Session):
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
    send_verification_email(user.email)
    
    # Try to verify with wrong code
    verify_data = {
        "email": user.email,
        "code": "000000"  # Wrong code
    }
    
    response = client.post("/api/auth/verify-email", json=verify_data)
    assert response.status_code == 400
    assert "Invalid or expired verification code" in response.json()["detail"]
    
    # Verify user is still unverified
    db.refresh(user)
    assert not user.is_verified

def test_verify_email_nonexistent_user():
    verify_data = {
        "email": "nonexistent@example.com",
        "code": "123456"
    }
    
    response = client.post("/api/auth/verify-email", json=verify_data)
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"] 