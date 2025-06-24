from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.models.player import Player
from app.models.user import User
from app.core.database import get_db
from app.services.auth_service import SECRET_KEY, ALGORITHM, get_current_player_from_token
from app.core.logging import logger

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)

async def get_current_player(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Player:
    """
    Get the current authenticated player from the JWT token.
    """
    logger.info(f"Getting current player from credentials: {credentials}")
    try:
        if not credentials:
            logger.info("No credentials provided")
            raise Exception("No authentication token provided")
        
        return get_current_player_from_token(credentials.credentials, db)
    except Exception as e:
        logger.error("Invalid authentication token. Exception: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",  # This message is important; it is used by the frontend axios intercepter.
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_logged_in_user(
    current_player: Player = Depends(get_current_player),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from the player.
    Use this when a logged in user is required.
    """
    if current_player.player_type.value != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Must be logged in - guest users not allowed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == current_player.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found in database",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def is_guest(player: Player) -> bool:
    """Check if the authenticated player is a guest."""
    return player.player_type.value == "guest"

def is_user(player: Player) -> bool:
    """Check if the authenticated player is a user."""
    return player.player_type.value == "user"

def get_user_id(entity: Player) -> Optional[int]:
    """Get the user ID if the entity is a user, None otherwise."""
    return entity.user_id if isinstance(entity, Player) and entity.player_type.value == "user" else None

def get_guest_id(entity: Player) -> Optional[int]:
    """Get the guest ID if the entity is a guest, None otherwise."""
    return entity.id if isinstance(entity, Player) and entity.player_type.value == "guest" else None
