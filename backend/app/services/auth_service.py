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

def create_guest(db: Session) -> Player:
    # Create guest session
    guest = Guest()
    db.add(guest)
    db.flush()  # Flush to get the guest ID
    
    # Create player profile for the guest
    player = Player(
        player_type=PlayerType.GUEST,
        guest_id=guest.id,
        display_name=guest.guest_name
    )
    db.add(player)
    db.commit()
    db.refresh(guest)
    db.refresh(player)
    logger.info("Created guest with id: %s", guest.id)
    logger.info("Created player with id: %s", player.id)
    
    return player


def create_access_token(data: dict, expire_minutes: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_player_token(player: Player) -> str:
    token_data = {
        "player_id": str(player.id),
        "player_type": player.player_type.value,
        "display_name": player.display_name,
    }
    
    # Add email and verification status for user players
    if player.player_type == PlayerType.USER and player.user:
        token_data["email"] = player.user.email
        token_data["is_verified"] = player.user.is_verified
    
    return create_access_token(
        data=token_data,
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


def get_current_player_from_token(token: str, db: Session) -> Player:
    """Get the current player from a JWT token (handles both user and guest tokens)."""
    invalid_player_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid player",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        player_id = payload.get("player_id")
        player_type = payload.get("player_type")
        
        if not player_id or not player_type:
            logger.error("Invalid player token. No player_id or player_type found.")
            raise Exception("Invalid player token. No player_id or player_type found.")
        
        # Find player by ID and type
        player = db.query(Player).filter(
            Player.id == int(player_id),
            Player.player_type == PlayerType(player_type)  # Convert string back to enum
        ).first()
            
        if not player:
            logger.error("Invalid player token. Player not found.")
            raise Exception("Invalid player token. Player not found.")
        
        return player
    except JWTError as e:
        logger.error("JWT Error while parsing token. Exception: %s", e)
        raise e


