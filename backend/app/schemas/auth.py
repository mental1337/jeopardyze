from pydantic import BaseModel, EmailStr
from typing import Optional

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

class GuestResponse(BaseModel):
    access_token: str 

class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    guest_id: Optional[str] = None


class RegisterResponse(BaseModel):
    message: str
    email: str

