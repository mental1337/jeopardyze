import random
import string
from datetime import datetime, timedelta, UTC
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

# In-memory storage for verification codes (in production, use Redis or similar)
verification_codes = {}

def generate_verification_code() -> str:
    """Generate a 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))

def store_verification_code(email: str, code: str):
    """Store verification code with expiration time (15 minutes)."""
    verification_codes[email] = {
        'code': code,
        'expires_at': datetime.now(UTC) + timedelta(minutes=15)
    }

def verify_code(email: str, code: str) -> bool:
    """Verify the code for the given email."""
    if email not in verification_codes:
        return False
    
    stored_data = verification_codes[email]
    if datetime.now(UTC) > stored_data['expires_at']:
        del verification_codes[email]
        return False
    
    if stored_data['code'] != code:
        return False
    
    # Code is valid, remove it from storage
    del verification_codes[email]
    return True

def send_verification_email(email: str) -> str:
    """
    Send verification email and return the verification code.
    In production, this would actually send an email.
    For development, we'll just return the code.
    """
    code = generate_verification_code()
    store_verification_code(email, code)
    
    # In production, send actual email here
    # TODO: Implement actual email sending
    print(f"Verification code for {email}: {code}")
    
    return code 