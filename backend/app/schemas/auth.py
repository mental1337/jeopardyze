from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    guest_id: Optional[str] = None

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    player_id: int
    display_name: str

class RegisterResponse(BaseModel):
    message: str
    email: str

class VerifyEmailResponse(BaseModel):
    access_token: str
    token_type: str
    player_id: int
    display_name: str

class GuestResponse(BaseModel):
    access_token: str 
    player_id: int
    display_name: str