from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class GuestSession(MyBaseModel):
    __tablename__ = "guest_sessions"
    
    session_token = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    converted_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    converted_to_user = relationship("User", back_populates="guest_sessions")
    game_sessions = relationship("GameSession", back_populates="guest_session")
    
    def __repr__(self):
        return f"<GuestSession(id={self.id}, session_token={self.session_token}, created_at={self.created_at})>" 