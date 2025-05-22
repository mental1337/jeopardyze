from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.logging import logger
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models import Question, QuizBoard, User, GameSession
from app.schemas import GameSessionResponse, AnswerQuestionResponse, AnswerQuestionRequest
from app.services.game_sessions_service import GameSessionsService


router = APIRouter(
    prefix="/api/game-sessions",
    tags=["game-sessions"]
)

   
@router.get("/{game_session_id}", response_model=GameSessionResponse)
async def get_game_session(game_session_id: int, db: Session = Depends(get_db)) -> GameSessionResponse:
    game_session = db.query(GameSession).filter(GameSession.id == game_session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    game_session_response = GameSessionsService.build_game_session_response(game_session)
    return game_session_response


@router.post("/new-from-quiz-board/{quiz_board_id}", response_model=GameSessionResponse)
async def create_game_session_from_quiz_board(quiz_board_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> GameSessionResponse:
    quiz_board = db.query(QuizBoard).filter(QuizBoard.id == quiz_board_id).first()
    if not quiz_board:
        logger.error(f"Couldn't create Game Session because Quiz board with id '{quiz_board_id}' not found")
        raise HTTPException(status_code=404, detail="Couldn't create Game Session because Quiz board with id '{quiz_board_id}' not found")

    game_session = GameSessionsService.create_from_quiz_board(quiz_board, user.id, db)
    game_session_response = GameSessionsService.build_game_session_response(game_session)
    return game_session_response


@router.post("/{game_session_id}/answer-question/{question_id}", response_model=AnswerQuestionResponse)
async def answer_question(game_session_id: int, question_id: int, answer_request: AnswerQuestionRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> AnswerQuestionResponse:
    logger.info(f"Answering question '{question_id}' for game session '{game_session_id}' with answer: '{answer_request.answer}'")
    response = GameSessionsService.answer_question(game_session_id, question_id, answer_request.answer, db, user)
    logger.info(f"Response: '{response}'")
    return response