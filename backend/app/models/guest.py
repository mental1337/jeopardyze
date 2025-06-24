from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

class Guest(MyBaseModel):
    __tablename__ = "guests"
    
    created_at = Column(DateTime, default=datetime.now)
    converted_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    player_profile = relationship("Player", back_populates="guest", uselist=False)
    converted_to_user = relationship("User", back_populates="guests")
    
    @hybrid_property
    def guest_name(self):
        """Generate guest name based on ID"""
        return f"Stranger-{self.id}" if self.id else "Stranger"
    
    def __repr__(self):
        return f"<Guest(id={self.id}, guest_name={self.guest_name}, created_at={self.created_at})>" 