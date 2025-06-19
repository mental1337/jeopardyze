from pydantic import BaseModel
from datetime import datetime
from typing import List

class SessionQuestionPyd(BaseModel):
    question_id: int
    question_text: str
    correct_answer: str | None = None
    points: int
    user_answer: str | None = None
    status: str = "unattempted"
    points_earned: int = 0

class SessionCategoryPyd(BaseModel):
    id: int
    name: str
    questions: List[SessionQuestionPyd]

class SessionQuizBoardPyd(BaseModel):
    id: int
    title: str
    categories: List[SessionCategoryPyd]

class GameSessionResponse(BaseModel):
    id: int
    user_id: int | None
    guest_id: int | None
    score: int
    started_at: datetime
    completed_at: datetime | None
    status: str
    session_quiz_board: SessionQuizBoardPyd

class AnswerQuestionRequest(BaseModel):
    answer: str

class AnswerQuestionResponse(BaseModel):
    question_id: int
    status: str
    correct_answer: str
    points_earned: int    
    updated_score: int
    game_status: str




