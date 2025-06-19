from sqlalchemy import Boolean, Column, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class User(MyBaseModel):
    __tablename__ = "users"
    
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for guest users
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    quiz_boards = relationship("QuizBoard", back_populates="created_by_user")
    game_sessions = relationship("GameSession", back_populates="user")
    guests = relationship("Guest", back_populates="converted_to_user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
