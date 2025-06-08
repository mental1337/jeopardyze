import random
import string
import os
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.config import secrets

# Mailgun configuration
MAILGUN_API_KEY = secrets.MAILGUN_API_KEY
DOMAIN = "jeopardyze.xyz"
MAILGUN_DOMAIN = "mg.jeopardyze.xyz"
MAILGUN_API_URL = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

# In-memory storage for verification codes (in production, use Redis or similar)
# TODO: Use Redis or similar for production
verification_codes = {}

def generate_verification_code() -> str:
    """Generate a 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))

def store_verification_code(email: str, code: str):
    """Store verification code with expiration time (15 minutes)."""
    verification_codes[email] = {
        'code': code,
        'expires_at': datetime.now(timezone.utc) + timedelta(minutes=15)
    }

def verify_code(email: str, code: str) -> bool:
    """Verify the code for the given email."""
    if email not in verification_codes:
        return False
    
    stored_data = verification_codes[email]
    if datetime.now(timezone.utc) > stored_data['expires_at']:
        del verification_codes[email]
        return False
    
    if stored_data['code'] != code:
        return False
    
    # Code is valid, remove it from storage
    del verification_codes[email]
    return True

def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Send an email using Mailgun API.
    Returns True if email was sent successfully, False otherwise.
    """
    if not MAILGUN_API_KEY:
        print("Warning: MAILGUN_API_KEY not set. Email not sent.")
        return False

    try:
        # TODO: Use httpx instead of requests for async support
        response = requests.post(
            MAILGUN_API_URL,
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Jeopardyze <noreply@{DOMAIN}>",
                "to": to_email,
                "subject": subject,
                "html": html_content
            }
        )
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_verification_email(email: str) -> str:
    """
    Send verification email and return the verification code.
    """
    code = generate_verification_code()
    store_verification_code(email, code)
    
    print(f"Verification code for {email}: {code}")
    # HTML email template
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #2c3e50;">Welcome to Jeopardyze!</h2>
            <p>Thank you for registering. Please use the following verification code to complete your registration:</p>
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
                <h1 style="color: #2c3e50; margin: 0; letter-spacing: 5px;">{code}</h1>
            </div>
            <p>This code will expire in 15 minutes.</p>
            <p>If you didn't request this verification code, please ignore this email.</p>
            <hr style="border: 1px solid #eee; margin: 20px 0;">
            <p style="color: #7f8c8d; font-size: 12px;">This is an automated message, please do not reply to this email.</p>
        </body>
    </html>
    """
    
    # Send the email
    success = send_email(
        to_email=email,
        subject="Verify your Jeopardyze account",
        html_content=html_content
    )
    
    if not success:
        print(f"Failed to send verification email to {email}")
    
    return code 


if __name__ == "__main__":
    print("Running email_verify_service.py as main script. Do this to test send an email.")
    email = "lkseyrenwindsor@gmail.com"
    print(f"Sending verification email to {email}")
    code = send_verification_email(email)
    if code:
        print(f"Email sent.Verification code: {code}")
    else:
        print("Failed to send email")