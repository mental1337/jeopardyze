from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    email: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    guest_session_token: str | None = None

class RegisterResponse(BaseModel):
    message: str
    email: str

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: str

class VerifyEmailResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    email: str 