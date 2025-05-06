from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class QuestionAttempt(MyBaseModel):
    __tablename__ = "question_attempts"
    
    game_session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=True, default=None)
    points_earned = Column(Integer, default=0)
    attempted_at = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="unattempted") # unattempted, attempted, correct, incorrect

    # Relationships
    game_session = relationship("GameSession", back_populates="question_attempts")
    question = relationship("Question", back_populates="question_attempts")
    