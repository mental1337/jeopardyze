from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import MyBaseModel, Base
import enum

class PlayerType(enum.Enum):
    USER = "user"
    GUEST = "guest"

class Player(MyBaseModel):
    __tablename__ = "players"
    
    player_type = Column(Enum(PlayerType), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    guest_id = Column(Integer, ForeignKey("guests.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="player_profile")
    guest = relationship("Guest", back_populates="player_profile")
    quiz_boards = relationship("QuizBoard", back_populates="created_by_player")
    game_sessions = relationship("GameSession", back_populates="player")
    
    def __repr__(self):
        if self.player_type == PlayerType.USER:
            return f"<Player(id={self.id}, type=user, user_id={self.user_id})>"
        else:
            return f"<Player(id={self.id}, type=guest, guest_id={self.guest_id})>"
    
    @property
    def display_name(self):
        """Get the display name of the player"""
        if self.player_type == PlayerType.USER and self.user:
            return self.user.username
        elif self.player_type == PlayerType.GUEST and self.guest:
            return self.guest.guest_name
        return "Unknown Player" 