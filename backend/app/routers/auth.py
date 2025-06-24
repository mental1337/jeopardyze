from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.auth_service import create_player_token, authenticate_user, create_guest, get_password_hash, ensure_player_exists
from app.services.email_verify_service import verify_code, send_verification_email
from app.models.user import User
from app.models.player import Player, PlayerType
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    VerifyEmailRequest,
    LoginResponse,
    RegisterResponse,
    VerifyEmailResponse,
    GuestResponse
)

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

@router.post("/guest", response_model=GuestResponse)
async def create_guest_endpoint(
    db: Session = Depends(get_db)
) -> GuestResponse:
    player = create_guest(db)
    return GuestResponse(
        access_token=create_player_token(player),
    )

@router.post("/register", response_model=LoginResponse)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
) -> LoginResponse:
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
    db.flush()  # Flush to get the user ID
    
    # Create player profile for the user
    player = Player(
        player_type=PlayerType.USER,
        user_id=user.id,
        display_name=user.username
    )
    db.add(player)
    db.commit()
    
    # Send verification email
    send_verification_email(db, request.email)
    
    token = create_player_token(player)
    return LoginResponse(
        access_token=token,
        is_verified=user.is_verified
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    # Verify the code
    if not verify_code(db, request.email, request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    # Mark user as verified
    user.is_verified = True
    db.commit()
    
    # Create new token for verified user
    player = ensure_player_exists(db, user)
    token = create_player_token(player)
    
    return VerifyEmailResponse(
        message="Email verified successfully",
        is_verified=user.is_verified,
        access_token=token
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
    
    player = ensure_player_exists(db, user)
    token = create_player_token(player)

    return LoginResponse(
        access_token=token,
        is_verified=user.is_verified
    ) 