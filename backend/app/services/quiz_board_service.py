from fastapi import HTTPException
from app.core.logging import logger
from app.models.quiz_board import QuizBoard
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models import Category, GameSession, Question, User
from app.services.llm_service import LLMService
from app.schemas.quiz_board import TopQuizBoardsResponse, TopQuizBoardModel


class QuizBoardService:
    @staticmethod
    def create_from_topic(topic: str, user_id: int, db: Session) -> QuizBoard:
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
                    points = 100
                    for q_data in cat_data["questions"]:
                        question = Question(
                            category_id=category.id,
                            question_text=q_data["question_text"],
                            correct_answer=q_data["correct_answer"],
                            points=points
                        )
                        db.add(question)
                        points += 100
                
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

    @staticmethod
    def get_top_quiz_boards(db: Session, limit: int = 10, offset: int = 0) -> TopQuizBoardsResponse:
        """
        Get top quiz boards sorted by number of game sessions, including top score information.
        """
        try:
            # First create a subquery for top scores with the most recent timestamp
            top_scores = (
                db.query(
                    GameSession.quiz_board_id,
                    GameSession.score,
                    GameSession.user_id,
                    GameSession.completed_at,
                    func.row_number().over(
                        partition_by=GameSession.quiz_board_id,
                        order_by=[
                            GameSession.score.desc(),
                            GameSession.completed_at.desc()  # Most recent first
                        ]
                    ).label('rn')
                )
                .subquery()
            )

            # Then use it in the main query
            quiz_boards = (
                db.query(
                    QuizBoard,
                    func.count(GameSession.id).label('total_sessions'),
                    top_scores.c.score.label('top_score'),
                    User.username.label('top_scorer')
                )
                .outerjoin(GameSession, QuizBoard.id == GameSession.quiz_board_id)
                .outerjoin(
                    top_scores,
                    (QuizBoard.id == top_scores.c.quiz_board_id) & 
                    (top_scores.c.rn == 1)  # Only get the top score
                )
                .outerjoin(
                    User,
                    User.id == top_scores.c.user_id
                )
                .group_by(QuizBoard.id, User.username, top_scores.c.score)
                .order_by(desc('total_sessions'))
                .limit(limit)
                .offset(offset)
                .all()
            )

            # Convert to response model
            top_quiz_boards = []
            for quiz_board, total_sessions, top_score, top_scorer in quiz_boards:
                top_quiz_boards.append(
                    TopQuizBoardModel(
                        id=quiz_board.id,
                        title=quiz_board.title,
                        creator=quiz_board.created_by_user.username,
                        total_sessions=total_sessions or 0,
                        top_score=top_score or 0,
                        top_scorer=top_scorer or "-",
                        created_at=quiz_board.created_at
                    )
                )

            return TopQuizBoardsResponse(
                quiz_boards=top_quiz_boards,
                total=len(top_quiz_boards),
                limit=limit,
                offset=offset
            )

        except Exception as e:
            logger.error(f"Failed to get top quiz boards: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to get top quiz boards. Error: {str(e)}"
            )