from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    points = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("Category", back_populates="questions")
    
    __table_args__ = (
        CheckConstraint('points > 0', name='valid_points'),
    )

Category.questions = relationship("Question", back_populates="category")

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    prompt = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    questions = relationship("Question", secondary="game_questions")

class GameQuestion(Base):
    __tablename__ = "game_questions"
    
    game_id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)

class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer, default=0)
    status = Column(String(20), default="in_progress")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    game = relationship("Game")
    user = relationship("User")
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('in_progress', 'completed', 'abandoned')",
            name='valid_status'
        ),
    )

class SessionAnswer(Base):
    __tablename__ = "session_answers"
    
    session_id = Column(Integer, ForeignKey("game_sessions.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    user_answer = Column(Text)
    is_correct = Column(Boolean)
    points_earned = Column(Integer)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    session = relationship("GameSession")
    question = relationship("Question")
