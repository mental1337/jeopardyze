from fastapi import APIRouter, Depends, HTTPException
from app.core.database import get_db
from app.models.game_session import GameSession
from app.models.question_attempt import QuestionAttempt
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List

router = APIRouter(
    prefix="/api/game-sessions",
    tags=["game-sessions"]
)

# class QuestionAttemptPydanticModel(BaseModel):
#     id: int
#     question_text: int
#     answer_text: str
#     status: str
#     points: int


class GameSessionResponse(BaseModel):
    id: int
    quiz_board_id: int
    user_id: int
    score: int
    status: str
    started_at: datetime
    completed_at: datetime
    # question_attempts: List[QuestionAttemptPydanticModel]
    
    class Config:
        from_attributes = True

    
router.get("/{game_session_id}", response_model=GameSessionResponse)
async def get_game_session(game_session_id: int, db: Session = Depends(get_db)) -> GameSession:
    game_session = db.query(GameSession).filter(GameSession.id == game_session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="Game session not found")
    return game_session
