from fastapi import HTTPException
from app.core.logging import logger
from app.models.quiz_board import QuizBoard
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.game_session import GameSession
from app.models.question import Question
from app.services.llm_service import LLMService

class QuizBoardService:
    @staticmethod
    async def create_from_topic(topic: str, user_id: int, db: Session) -> QuizBoard:
        # Check if the same topic already exists in the database
        quiz_board = db.query(QuizBoard).filter(QuizBoard.source_content == topic).first()
        if quiz_board:
            logger.info(f"Quiz board already exists for topic: {topic}, reusing it")

        if not quiz_board:
            # Generate the quiz board
            logger.info(f"Generating quiz board from LLM service for topic: {topic}")
            try:
                llm_service = LLMService()
                quiz_data = llm_service.generate_quiz_board_from_topic(topic)
            except Exception as e:
                logger.error(f"Failed to generate quiz board: {str(e)}")
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
                created_by_user_id=user_id
            )
            
            # Add quiz data to the database
            logger.info(f"Adding new quiz board to the database")
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
                            answer_text=q_data["answer"],
                            points=q_data["points"]
                        )
                        db.add(question)
                
                db.commit()
                db.refresh(quiz_board)

            except Exception as e:
                db.rollback()
                logger.error(f"Failed to add quiz board to database: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to add the generated quiz board to the database. Error: {str(e)}"
                )

        logger.info(f"Successfully created quiz board. Quiz Board ID: {quiz_board.id}")

        return quiz_board