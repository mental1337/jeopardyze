from typing import Union, Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.models.user import User
from app.models.guest import Guest
from app.core.database import get_db
from app.services.auth_service import SECRET_KEY, ALGORITHM
from app.core.logging import logger

# Create a union type for authenticated entities
AuthenticatedEntity = Union[User, Guest]

# Security scheme for Bearer token
security = HTTPBearer(auto_error=False)

async def get_current_user_or_guest(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> AuthenticatedEntity:
    """
    Get the current authenticated user or guest from the JWT token.
    Returns None if no valid token is provided (for optional authentication).
    """
    logger.info(f"Getting current user or guest from credentials: {credentials}")
    if not credentials:
        logger.info("No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded payload: {payload}")
        subject = payload.get("sub")
        
        if subject == "guest":
            # Handle guest authentication
            guest_id = payload.get("guest_id")
            if not guest_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid guest token: missing guest_id",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            guest = db.query(Guest).filter(Guest.id == int(guest_id)).first()
            if not guest:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Guest not found in database",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return guest
        else:
            # Handle user authentication
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid user token: missing user_id",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user = db.query(User).filter(User.id == int(user_id)).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found in database",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return user
            
    except JWTError as e:
        logger.error("JWT Error while parsing token. Invalid token. Exception: %s", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_logged_in_user(
    current_user: Optional[AuthenticatedEntity] = Depends(get_current_user_or_guest)
) -> User:
    """
    Get the current authenticated logged in user.
    Use this when a logged in user is required.
    """
    if not current_user or not isinstance(current_user, User):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No logged in user found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user   


def is_guest(entity: AuthenticatedEntity) -> bool:
    """Check if the authenticated entity is a guest."""
    return isinstance(entity, Guest)

def is_user(entity: AuthenticatedEntity) -> bool:
    """Check if the authenticated entity is a user."""
    return isinstance(entity, User)

def get_user_id(entity: AuthenticatedEntity) -> Optional[int]:
    """Get the user ID if the entity is a user, None otherwise."""
    return entity.id if isinstance(entity, User) else None

def get_guest_id(entity: AuthenticatedEntity) -> Optional[int]:
    """Get the guest ID if the entity is a guest, None otherwise."""
    return entity.id if isinstance(entity, Guest) else None
