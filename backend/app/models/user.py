from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class User(MyBaseModel):
    __tablename__ = "users"
    
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    quiz_boards = relationship("QuizBoard", back_populates="created_by_user")
    game_sessions = relationship("GameSession", back_populates="user")
    
    