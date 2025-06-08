import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
import requests

from app.services.email_verify_service import (
    generate_verification_code,
    store_verification_code,
    verify_code,
    send_email,
    send_verification_email,
    verification_codes
)

def test_generate_verification_code():
    """Test that verification code is generated correctly."""
    code = generate_verification_code()
    print("Generated code: ", code)
    assert len(code) == 6
    assert code.isdigit()

def test_store_verification_code():
    """Test storing verification code with expiration."""
    email = "test@example.com"
    code = "123456"
    
    store_verification_code(email, code)
    print("Stored code: ", verification_codes)
    assert email in verification_codes
    assert verification_codes[email]['code'] == code
    assert isinstance(verification_codes[email]['expires_at'], datetime)

def test_verify_code_valid():
    """Test verification of a valid code."""
    email = "test@example.com"
    code = "123456"
    
    # Store a code that hasn't expired
    verification_codes[email] = {
        'code': code,
        'expires_at': datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    
    assert verify_code(email, code) is True
    assert email not in verification_codes  # Code should be removed after verification

def test_verify_code_invalid():
    """Test verification of an invalid code."""
    email = "test@example.com"
    code = "123456"
    wrong_code = "654321"
    
    # Store a code that hasn't expired
    verification_codes[email] = {
        'code': code,
        'expires_at': datetime.now(timezone.utc) + timedelta(minutes=15)
    }
    
    assert verify_code(email, wrong_code) is False
    assert email in verification_codes  # Code should remain if verification fails

def test_verify_code_expired():
    """Test verification of an expired code."""
    email = "test@example.com"
    code = "123456"
    
    # Store an expired code
    verification_codes[email] = {
        'code': code,
        'expires_at': datetime.now(timezone.utc) - timedelta(minutes=1)
    }
    
    assert verify_code(email, code) is False
    assert email not in verification_codes  # Expired code should be removed

def test_verify_code_nonexistent_email():
    """Test verification for non-existent email."""
    assert verify_code("nonexistent@example.com", "123456") is False

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
def test_send_verification_email(mock_send_email):
    """Test sending verification email."""
    email = "test@example.com"
    mock_send_email.return_value = True
    
    code = send_verification_email(email)
    
    assert len(code) == 6
    assert code.isdigit()
    assert email in verification_codes
    mock_send_email.assert_called_once()
    
    # Verify email content
    call_args = mock_send_email.call_args[1]
    assert call_args['to_email'] == email
    assert "Verify your Jeopardyze account" in call_args['subject']
    assert code in call_args['html_content']

@patch('app.services.email_verify_service.send_email')
def test_send_verification_email_failure(mock_send_email):
    """Test failed verification email sending."""
    email = "test@example.com"
    mock_send_email.return_value = False
    
    code = send_verification_email(email)
    
    assert len(code) == 6
    assert code.isdigit()
    assert email in verification_codes
    mock_send_email.assert_called_once() 