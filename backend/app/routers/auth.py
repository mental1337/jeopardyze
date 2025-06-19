from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import create_access_token, authenticate_user, create_guest_session, get_password_hash, create_user_access_token
from app.services.email_verify_service import verify_code, send_verification_email
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    VerifyEmailRequest,
    UserResponse,
    LoginResponse,
    RegisterResponse,
    VerifyEmailResponse,
    GuestResponse
)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/guest-session", response_model=GuestResponse)
async def create_guest_session_endpoint(
    db: Session = Depends(get_db)
) -> GuestResponse:
    token = create_guest_session(db)
    return GuestResponse(
        access_token=token
    )

@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
) -> RegisterResponse:
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        username=request.username,
        email=request.email,
        password_hash=get_password_hash(request.password),
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    # Send verification email
    send_verification_email(request.email)
    
    return RegisterResponse(
        message="Verification code sent to email",
        email=request.email
    )

@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db)
) -> VerifyEmailResponse:
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify the code
    if not verify_code(request.email, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )
    
    # Mark user as verified
    user.is_verified = True
    db.commit()
    
    # Create access token using the new function
    access_token = create_user_access_token(user)
    
    return VerifyEmailResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email
    )

@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
) -> LoginResponse:
    user = authenticate_user(db, request.username_or_email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token using the new function
    token = create_user_access_token(user)
    
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        username=user.username,
        email=user.email
    ) 