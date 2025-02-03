from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    category_id: int
    question_text: str
    answer_text: str
    points: int = Field(..., gt=0)

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Game Schemas
class GameBase(BaseModel):
    prompt: Optional[str] = None

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    created_by_user_id: int
    created_at: datetime
    questions: List[Question] = []

    class Config:
        from_attributes = True

# Game Session Schemas
class GameSessionBase(BaseModel):
    game_id: int
    user_id: int

class GameSessionCreate(GameSessionBase):
    pass

class GameSession(GameSessionBase):
    id: int
    score: int = 0
    status: str = "in_progress"
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Answer Submission Schema
class AnswerSubmission(BaseModel):
    question_id: int
    user_answer: str

# Session Answer Schema
class SessionAnswer(BaseModel):
    session_id: int
    question_id: int
    user_answer: str
    is_correct: bool
    points_earned: int
    answered_at: datetime

    class Config:
        from_attributes = True

# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
