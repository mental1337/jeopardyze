from pydantic import BaseModel, EmailStr
from typing import Optional

class GuestResponse(BaseModel):
    access_token: str 

    
class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str


class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str

class VerifyEmailResponse(BaseModel):
    message: str
    access_token: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    guest_id: Optional[str] = None

RegisterResponse = LoginResponse