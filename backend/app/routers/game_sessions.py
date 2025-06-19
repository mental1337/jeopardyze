from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.logging import logger
from app.core.database import get_db
from app.core.auth import get_current_user_or_guest, AuthenticatedEntity, get_user_id, get_guest_id
from app.models import Question, QuizBoard, User, GameSession, Guest
from app.schemas import GameSessionResponse, AnswerQuestionResponse, AnswerQuestionRequest
from app.services.game_sessions_service import GameSessionsService


router = APIRouter(
    prefix="/api/game-sessions",
    tags=["game-sessions"]
)

@router.get("/existing")
async def get_existing_game_session(
    quiz_board_id: int = Query(..., description="ID of the quiz board"),
    user_id: Optional[int] = Query(None, description="ID of the user"),
    guest_id: Optional[int] = Query(None, description="ID of the guest"),
    db: Session = Depends(get_db)
) -> Dict:
    """
    Find an existing active game session for a user/guest and quiz board.
    Returns None if no active session exists.
    """
    # Verify quiz board exists
    quiz_board = db.query(QuizBoard).filter(QuizBoard.id == quiz_board_id).first()
    if not quiz_board:
        raise HTTPException(status_code=404, detail=f"Quiz board with id '{quiz_board_id}' not found")

    # Build query based on whether we're looking for a user or guest session
    query = db.query(GameSession).filter(
        GameSession.quiz_board_id == quiz_board_id,
    )

    if user_id is not None:
        query = query.filter(GameSession.user_id == user_id)
    elif guest_id is not None:
        query = query.filter(GameSession.guest_id == guest_id)
    else:
        raise HTTPException(
            status_code=400,
            detail="Either user_id or guest_id must be provided"
        )

    # Get the most recent session if multiple exist
    game_session = query.order_by(GameSession.created_at.desc()).first()

    if not game_session:
        return {}

    return {
        "game_session_id": game_session.id
    }

@router.get("/{game_session_id}", response_model=GameSessionResponse)
async def get_game_session(game_session_id: int, db: Session = Depends(get_db)) -> GameSessionResponse:
    game_session = db.query(GameSession).filter(GameSession.id == game_session_id).first()
    if not game_session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    game_session_response = GameSessionsService.build_game_session_response(game_session)
    return game_session_response


@router.post("/new-from-quiz-board/{quiz_board_id}")
async def create_game_session_from_quiz_board(
    quiz_board_id: int,
    db: Session = Depends(get_db),
    current_user: AuthenticatedEntity = Depends(get_current_user_or_guest)
) -> Dict:
    quiz_board = db.query(QuizBoard).filter(QuizBoard.id == quiz_board_id).first()
    if not quiz_board:
        logger.error(f"Couldn't create Game Session because Quiz board with id '{quiz_board_id}' not found")
        raise HTTPException(status_code=404, detail="Couldn't create Game Session because Quiz board with id '{quiz_board_id}' not found")

    # Extract user_id or guest_id from the authenticated entity
    user_id = get_user_id(current_user)
    guest_id = get_guest_id(current_user)
    
    game_session = GameSessionsService.create_from_quiz_board(quiz_board, user_id, guest_id, db)
    return {
        "game_session_id": game_session.id
    }


@router.post("/{game_session_id}/answer-question/{question_id}", response_model=AnswerQuestionResponse)
async def answer_question(
    game_session_id: int, 
    question_id: int, 
    answer_request: AnswerQuestionRequest, 
    db: Session = Depends(get_db), 
    current_user: AuthenticatedEntity = Depends(get_current_user_or_guest)
) -> AnswerQuestionResponse:
    logger.info(f"Answering question '{question_id}' for game session '{game_session_id}' with answer: '{answer_request.answer}'")
    response = GameSessionsService.answer_question(game_session_id, question_id, answer_request.answer, db, current_user)
    logger.info(f"Response: '{response}'")
    return response