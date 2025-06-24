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
    display_name = Column(String, nullable=False)

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
    