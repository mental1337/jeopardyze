from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.models.game_session import GameSession
from app.models.question_attempt import QuestionAttempt
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.routers.quiz_boards import QuizBoardPydanticModel

router = APIRouter(
    prefix="/api/game-sessions",
    tags=["game-sessions"]
)


class SessionQuestionPyd(BaseModel):
    question_id: int
    question_text: str
    answer_text: str
    points: int
    
    user_answer: str | None = None
    status: str = "unattempted"
    is_correct: bool | None = None
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
    user_id: int
    score: int
    started_at: datetime
    completed_at: datetime | None
    status: str

    session_quiz_board: SessionQuizBoardPyd
    
    class Config:
        from_attributes = True

    
@router.get("/{game_session_id}", response_model=GameSessionResponse)
async def get_game_session(game_session_id: int, db: Session = Depends(get_db)) -> GameSessionResponse:
    game_session = db.query(GameSession).filter(GameSession.id == game_session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    
    session_quiz_board = SessionQuizBoardPyd(id=game_session.quiz_board.id, title=game_session.quiz_board.title, categories=[])

    # Create a dictionary of corresponding question attempts indexed by question_id
    question_attempts_dict = {
        attempt.question_id: attempt 
        for attempt in game_session.question_attempts
    }

    for category in game_session.quiz_board.categories:
        session_category = SessionCategoryPyd(id=category.id, name=category.name, questions=[])
        for question in category.questions:
            question_attempt = question_attempts_dict.get(question.id)
            
            session_question = SessionQuestionPyd(
                question_id=question.id,
                question_text=question.question_text,
                answer_text=question.answer_text,
                points=question.points
            )

            if question_attempt:
                session_question.user_answer = question_attempt.user_answer
                session_question.status = question_attempt.status
                session_question.is_correct = question_attempt.is_correct
                session_question.points_earned = question_attempt.points_earned

            session_category.questions.append(session_question)
        session_quiz_board.categories.append(session_category)


    # Create the response object with explicit field mapping
    game_session_response = GameSessionResponse(
        id=game_session.id,
        user_id=game_session.user_id,
        score=game_session.score,
        started_at=game_session.started_at,
        completed_at=game_session.completed_at,
        status=game_session.status,
        session_quiz_board=session_quiz_board
    )

    return game_session_response

