from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Form, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.logging import logger
from app.models import QuizBoard, User
from app.schemas import QuizBoardPydanticModel, TopQuizBoardsResponse, QuizBoardPydanticModel
from app.services.quiz_board_service import QuizBoardService
from app.services.game_sessions_service import GameSessionsService

router = APIRouter(
    prefix="/api/quiz-boards",
    tags=["quiz-boards"]
)


@router.get("", response_model=List[QuizBoardPydanticModel])
async def get_all_quiz_boards(db: Session = Depends(get_db), search: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[QuizBoard]:
    query = db.query(QuizBoard)

    if search:
        query = query.filter(QuizBoard.title.ilike(f"%{search}%"))
    
    query.limit(limit).offset(offset)
    quiz_boards = query.all()

    return quiz_boards


####

@router.post("/from-topic")
async def create_quiz_board_from_topic(
    topic: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
) -> Dict:
    quiz_board = QuizBoardService.create_from_topic(topic, user.id, db)
    game_session = GameSessionsService.create_from_quiz_board(quiz_board, user.id, db)
    
    return {
        "game_session_id": game_session.id
    }


# @router.post("/from-document")
# async def create_quiz_from_document(
#     file: UploadFile = File(None),
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Read the file contents and return the text
#     file_contents = await file.read()

#     return {"message": "This shall create a quiz board from a document", 
#             "file.filename": file.filename,
#             "file.size": file.size,
#             "file.content_type": file.content_type,
#             "file.headers": file.headers,
#             "file_contents": file_contents,
#             "file.file": file.file
#             }


## Endpoint: GET /api/quiz-boards/top?limit=10&offset=0
@router.get("/top", response_model=TopQuizBoardsResponse)
async def get_top_quiz_boards(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
) -> TopQuizBoardsResponse:
    """
    Get top quiz boards sorted by number of game sessions, including top score information.
    """
    return QuizBoardService.get_top_quiz_boards(db, limit, offset)



