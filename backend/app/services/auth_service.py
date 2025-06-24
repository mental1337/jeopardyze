from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.models.guest import Guest
from app.models.player import Player, PlayerType
from app.core.config import settings, secrets
from app.core.logging import logger

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = secrets.JWT_SECRET_KEY
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expire_minutes: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_guest(db: Session) -> Player:
    # Create guest session
    guest = Guest()
    db.add(guest)
    db.flush()  # Flush to get the guest ID
    
    # Create player profile for the guest
    player = Player(
        player_type=PlayerType.GUEST,
        guest_id=guest.id
    )
    db.add(player)
    db.commit()
    db.refresh(guest)
    db.refresh(player)
    logger.info("Created guest with id: %s", guest.id)
    logger.info("Created player with id: %s", player.id)
    
    return player

# def create_user_access_token(user: User) -> str:
#     """Create a JWT token for an authenticated user."""
#     return create_access_token(
#         data={
#             "sub": str(user.id),
#             "username": user.username,
#             "email": user.email
#         },
#         expire_minutes=60*24*7 # 7 days
#     )

def create_player_token(player: Player) -> str:
    return create_access_token(
        data={
            "player_id": str(player.id),
            "player_type": player.player_type.value,
            "display_name": player.display_name
        },
        expire_minutes=60*24*30 # 30 days
    )

def ensure_player_exists(db: Session, user: User) -> Player:
    """Ensure a Player record exists for the user, create if it doesn't."""
    existing_player = db.query(Player).filter(Player.user_id == user.id).first()
    if existing_player:
        return existing_player
    
    # Create player profile for the user
    player = Player(
        player_type=PlayerType.USER,
        user_id=user.id
    )
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    # Try to find user by username or email
    user = db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    
    # Ensure player record exists
    ensure_player_exists(db, user)
    return user

def get_current_user_from_token(token: str, db: Session) -> User:
    """Get the current user from a JWT token. For backward compatibility."""
    player = get_current_player_from_token(token, db)
    
    # Ensure this is a user player, not a guest
    if player.player_type != PlayerType.USER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is for guest user, not authenticated user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get the associated user
    user = db.query(User).filter(User.id == player.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_player_from_token(token: str, db: Session) -> Player:
    """Get the current player from a JWT token (handles both user and guest tokens)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        player_id = payload.get("player_id")
        player_type = payload.get("player_type")
        
        if not player_id or not player_type:
            raise credentials_exception
            
        # Find player by ID and type
        player = db.query(Player).filter(
            Player.id == int(player_id),
            Player.player_type == PlayerType(player_type)  # Convert string back to enum
        ).first()
            
        if not player:
            raise credentials_exception
        return player
        
    except JWTError:
        raise credentials_exception

