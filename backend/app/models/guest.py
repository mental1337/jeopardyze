from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class Guest(MyBaseModel):
    __tablename__ = "guests"
    
    created_at = Column(DateTime, default=datetime.now)
    converted_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    converted_to_user = relationship("User", back_populates="guests")
    game_sessions = relationship("GameSession", back_populates="guest")
    
    def __repr__(self):
        return f"<Guest(id={self.id}, created_at={self.created_at})>" 