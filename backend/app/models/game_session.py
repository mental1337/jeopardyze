from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class GameSession(MyBaseModel):
    __tablename__ = "game_sessions"
    
    quiz_board_id = Column(Integer, ForeignKey("quiz_boards.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="in_progress")

    # Relationships
    quiz_board = relationship("QuizBoard", back_populates="game_sessions")
    user = relationship("User", back_populates="game_sessions")
    