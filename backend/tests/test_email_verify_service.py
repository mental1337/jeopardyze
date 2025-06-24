import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import requests
from sqlalchemy.orm import Session

from app.services.email_verify_service import (
    generate_verification_code,
    store_verification_code,
    verify_code,
    send_email,
    send_verification_email
)
from app.models.user import User

def test_generate_verification_code():
    """Test that verification code is generated correctly."""
    code = generate_verification_code()
    print("Generated code: ", code)
    assert len(code) == 6
    assert code.isdigit()

def test_store_verification_code(db: Session):
    """Test storing verification code in database."""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    email = "test@example.com"
    code = "123456"
    
    store_verification_code(db, email, code)
    
    # Verify the code was stored
    db.refresh(user)
    assert user.verification_code == code

def test_store_verification_code_user_not_found(db: Session):
    """Test storing verification code for non-existent user."""
    email = "nonexistent@example.com"
    code = "123456"
    
    with pytest.raises(ValueError, match=f"User with email {email} not found"):
        store_verification_code(db, email, code)

def test_verify_code_valid(db: Session):
    """Test verification of a valid code."""
    # Create a test user with verification code
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        is_verified=False,
        verification_code="123456"
    )
    db.add(user)
    db.commit()
    
    email = "test@example.com"
    code = "123456"
    
    assert verify_code(db, email, code) is True
    
    # Verify the code was cleared after successful verification
    db.refresh(user)
    assert user.verification_code is None

def test_verify_code_invalid(db: Session):
    """Test verification of an invalid code."""
    # Create a test user with verification code
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        is_verified=False,
        verification_code="123456"
    )
    db.add(user)
    db.commit()
    
    email = "test@example.com"
    wrong_code = "654321"
    
    assert verify_code(db, email, wrong_code) is False
    
    # Verify the code was not cleared after failed verification
    db.refresh(user)
    assert user.verification_code == "123456"

def test_verify_code_nonexistent_email(db: Session):
    """Test verification for non-existent email."""
    assert verify_code(db, "nonexistent@example.com", "123456") is False

def test_verify_code_no_verification_code(db: Session):
    """Test verification for user without verification code."""
    # Create a test user without verification code
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        is_verified=False,
        verification_code=None
    )
    db.add(user)
    db.commit()
    
    assert verify_code(db, "test@example.com", "123456") is False

@patch('app.services.email_verify_service.requests.post')
def test_send_email_success(mock_post):
    """Test successful email sending."""
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response
    
    result = send_email(
        to_email="test@example.com",
        subject="Test Subject",
        html_content="<p>Test content</p>"
    )
    
    assert result is True
    mock_post.assert_called_once()

@patch('app.services.email_verify_service.requests.post')
def test_send_email_failure(mock_post):
    """Test failed email sending."""
    mock_post.side_effect = requests.exceptions.RequestException("Request Exception")
    
    result = send_email(
        to_email="test@example.com",
        subject="Test Subject",
        html_content="<p>Test content</p>"
    )
    
    assert result is False

@patch('app.services.email_verify_service.send_email')
def test_send_verification_email(db: Session, mock_send_email):
    """Test sending verification email."""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    email = "test@example.com"
    mock_send_email.return_value = True
    
    code = send_verification_email(db, email)
    
    assert len(code) == 6
    assert code.isdigit()
    
    # Verify the code was stored in the database
    db.refresh(user)
    assert user.verification_code == code
    
    mock_send_email.assert_called_once()
    
    # Verify email content
    call_args = mock_send_email.call_args[1]
    assert call_args['to_email'] == email
    assert "Verify your Jeopardyze account" in call_args['subject']
    assert code in call_args['html_content']

@patch('app.services.email_verify_service.send_email')
def test_send_verification_email_failure(db: Session, mock_send_email):
    """Test failed verification email sending."""
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    email = "test@example.com"
    mock_send_email.return_value = False
    
    code = send_verification_email(db, email)
    
    assert len(code) == 6
    assert code.isdigit()
    
    # Verify the code was still stored in the database even if email failed
    db.refresh(user)
    assert user.verification_code == code
    
    mock_send_email.assert_called_once() 