from datetime import datetime
from pydantic import BaseModel
from typing import List

class TopQuizBoardModel(BaseModel):
    id: int
    title: str
    total_sessions: int
    top_score: int
    top_score_username: str
    created_at: datetime

    class Config:
        from_attributes = True

class TopQuizBoardsResponse(BaseModel):
    quiz_boards: List[TopQuizBoardModel]
    total: int
    limit: int
    offset: int


class QuestionPydanticModel(BaseModel):
    id: int
    question_text: str
    correct_answer: str
    points: int

class CategoryPydanticModel(BaseModel):
    id: int
    name: str
    questions: List[QuestionPydanticModel]

class QuizBoardPydanticModel(BaseModel):
    id: int
    title: str
    source_type: str
    source_content: str
    created_by_user_id: int
    created_at: datetime
    categories: List[CategoryPydanticModel]

    class Config:
        from_attributes = True  # This allows the model to be initialized from SQLAlchemy models by matching the attributes
