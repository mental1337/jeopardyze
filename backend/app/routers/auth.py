from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_password_hash
)
from app.services.email_verify_service import send_verification_email, verify_code
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    VerifyEmailRequest,
    VerifyEmailResponse
)
from app.models.user import User

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
) -> LoginResponse:
    user = authenticate_user(db, login_request.username_or_email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
    )
    
    return LoginResponse(
        access_token=access_token,
        user_id=user.id,
        username=user.username,
        email=user.email
    )

@router.post("/register", response_model=RegisterResponse)
async def register(
    register_request: RegisterRequest,
    db: Session = Depends(get_db)
) -> RegisterResponse:
    # Check if username is already taken
    if db.query(User).filter(User.username == register_request.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already registered"
        )
    
    # Check if email is already taken
    if db.query(User).filter(User.email == register_request.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    
    # Create new user
    user = User(
        username=register_request.username,
        email=register_request.email,
        password_hash=get_password_hash(register_request.password),
        is_verified=False
    )
    db.add(user)
    db.commit()
    
    # Send verification email
    send_verification_email(register_request.email)
    
    return RegisterResponse(
        message="Verification code sent to email",
        email=register_request.email
    )

@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(
    verify_request: VerifyEmailRequest,
    db: Session = Depends(get_db)
) -> VerifyEmailResponse:
    # Find user by email
    user = db.query(User).filter(User.email == verify_request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify the code
    if not verify_code(verify_request.email, verify_request.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )
    
    # Mark user as verified
    user.is_verified = True
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    
    return VerifyEmailResponse(
        access_token=access_token,
        user_id=user.id,
        username=user.username,
        email=user.email
    ) 