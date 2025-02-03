from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..routers.auth import get_current_user

router = APIRouter(prefix="/games", tags=["Games"])

@router.post("/", response_model=schemas.Game)
async def create_game(
    game: schemas.GameCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_game = models.Game(prompt=game.prompt, created_by_user_id=current_user.id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/", response_model=List[schemas.Game])
async def list_games(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    games = db.query(models.Game).offset(skip).limit(limit).all()
    return games

@router.get("/{game_id}", response_model=schemas.Game)
async def get_game(
    game_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/{game_id}/start", response_model=schemas.GameSession)
async def start_game_session(
    game_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    
    session = models.GameSession(
        game_id=game_id,
        user_id=current_user.id,
        status="in_progress"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

@router.post("/sessions/{session_id}/answer", response_model=schemas.SessionAnswer)
async def submit_answer(
    session_id: int,
    answer: schemas.AnswerSubmission,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    session = db.query(models.GameSession).filter(
        models.GameSession.id == session_id,
        models.GameSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Game session not found")
    
    if session.status != "in_progress":
        raise HTTPException(status_code=400, detail="Game session is not in progress")
    
    # Get the question
    question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if answer was already submitted
    existing_answer = db.query(models.SessionAnswer).filter(
        models.SessionAnswer.session_id == session_id,
        models.SessionAnswer.question_id == answer.question_id
    ).first()
    
    if existing_answer:
        raise HTTPException(status_code=400, detail="Answer already submitted for this question")
    
    # Simple string comparison for answer validation (can be improved)
    is_correct = answer.user_answer.lower().strip() == question.answer_text.lower().strip()
    points_earned = question.points if is_correct else 0
    
    # Record the answer
    session_answer = models.SessionAnswer(
        session_id=session_id,
        question_id=answer.question_id,
        user_answer=answer.user_answer,
        is_correct=is_correct,
        points_earned=points_earned
    )
    db.add(session_answer)
    
    # Update session score
    session.score += points_earned
    db.commit()
    db.refresh(session_answer)
    
    return session_answer
