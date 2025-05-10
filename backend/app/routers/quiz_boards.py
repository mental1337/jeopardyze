from typing import Optional, List
from fastapi import APIRouter, Depends, Form, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user
from app.services.llm_service import LLMService
from backend.app.models.category import Category
from backend.app.models.question import Question
from backend.app.models.quiz_board import QuizBoard
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/api/quiz-boards",
    tags=["quiz-boards"]
)

class QuestionPydanticModel(BaseModel):
    id: int
    question_text: str
    answer: str
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


@router.post("/from-topic", response_model=QuizBoardPydanticModel)
async def create_quiz_board_from_topic(
    topic: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> QuizBoard: # This function returns QuizBoard object, which the decorator will convert to QuizBoardPydanticModel. Technically, doesn't matter.
    
    # Check if the same topic already exists in the database
    existing_quiz_board = db.query(QuizBoard).filter(QuizBoard.source_content == topic).first()
    if existing_quiz_board:
        # Return the existing quiz board
        return existing_quiz_board
    
    # Generate the quiz board
    try:
        llm_service = LLMService()
        quiz_data = llm_service.generate_quiz_board_from_topic(topic)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get response from LLM. Error: {e}")

    # quiz_data is a json object of the following format:
    # {
    #     "title": "Quiz Title",
    #     "categories": [
    #         {
    #             "name": "Category Name",
    #             "questions": [
    #                 {
    #                     "question_text": "Question Text",
    #                     "answer": "Answer Text",
    #                     "points": 100
    #                 },
    #                 ...
    #             ]
    #         },
    #         ...
    #     ]
    # }

    # Create quiz board in database
    quiz_board = QuizBoard(
        title=quiz_data["title"],
        source_type="topic",
        source_content=topic,
        created_by_user_id=current_user.id
    )
    
    # Add quiz data to the databasE
    try:
        db.add(quiz_board)
        db.flush()
        
        # Create categories and questions
        for cat_data in quiz_data["categories"]:
            category = Category(
                name=cat_data["name"],
                quiz_board_id=quiz_board.id
            )
            db.add(category)
            db.flush()
            
            # Create questions for this category
            for q_data in cat_data["questions"]:
                question = Question(
                    category_id=category.id,
                    question_text=q_data["question_text"],
                    answer=q_data["answer"],
                    points=q_data["points"]
                )
                db.add(question)
        
        # Commit all changes
        db.commit()
        db.refresh(quiz_board)
        
        return quiz_board
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add the generated quiz board to the database. Error: {str(e)}"
        )



# @router.post("/from-document")
# async def create_quiz_from_document(
#     file: UploadFile = File(None),
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)
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



