import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.user import User
from app.services.auth_service import get_password_hash

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