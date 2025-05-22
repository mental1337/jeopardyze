from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Form, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.llm_service import LLMService
from app.models.category import Category
from app.models.question import Question
from app.models.quiz_board import QuizBoard
from app.models.game_session import GameSession
from app.core.logging import logger
from pydantic import BaseModel
from datetime import datetime
from app.models.user import User
from app.services.quiz_board_service import QuizBoardService

router = APIRouter(
    prefix="/api/quiz-boards",
    tags=["quiz-boards"]
)



class QuestionPydanticModel(BaseModel):
    id: int
    question_text: str
    answer_text: str
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


@router.get("", response_model=List[QuizBoardPydanticModel])
async def get_quiz_boards(db: Session = Depends(get_db), search: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[QuizBoard]:
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
    current_user: User = Depends(get_current_user)
) -> Dict:
    quiz_board = QuizBoardService.create_from_topic(topic, current_user.id, db)

    return {
        "quiz_board_id": quiz_board.id
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



