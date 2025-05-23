from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
# from app.models.game_session import GameSession
from app.models import GameSession, Question, QuestionAttempt, User, QuizBoard
from app.schemas import GameSessionResponse, SessionQuizBoardPyd, SessionCategoryPyd, SessionQuestionPyd, AnswerQuestionResponse
from app.core.logging import logger

class GameSessionsService:
    @staticmethod
    def create_from_quiz_board(quiz_board: QuizBoard, user_id: int, db: Session) -> GameSession:        
        game_session = GameSession(
            user_id=user_id,
            quiz_board_id=quiz_board.id
        )
        db.add(game_session)
        db.commit()
        db.refresh(game_session)

        return game_session

    @staticmethod
    def build_game_session_response(game_session: GameSession) -> GameSessionResponse:    
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
                    points=question.points
                )

                if question_attempt:
                    session_question.user_answer = question_attempt.user_answer
                    session_question.status = question_attempt.status
                    session_question.points_earned = question_attempt.points_earned
                    session_question.answer_text = question.answer_text # Only return this if the question has been answered

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

    @staticmethod
    def answer_question(game_session_id: int, question_id: int, answer: str, db: Session, user: User) -> AnswerQuestionResponse:
        game_session = db.query(GameSession).filter(GameSession.id == game_session_id).first()
        if not game_session:
            raise HTTPException(status_code=404, detail="Game session not found")

        question = db.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        question_attempt = db.query(QuestionAttempt).filter(QuestionAttempt.game_session_id == game_session_id, QuestionAttempt.question_id == question_id).first()
        if question_attempt:
            raise HTTPException(status_code=400, detail="Question already answered")

        is_correct = question.answer_text == answer
        status = "correct" if is_correct else "incorrect"
        points_earned = question.points if is_correct else 0
        updated_score = game_session.score + points_earned
        
        question_attempt = QuestionAttempt(
            game_session_id=game_session_id,
            question_id=question_id,
            user_answer=answer,
            status=status,
            points_earned=points_earned
        )

        db.add(question_attempt)
        db.commit()
        db.refresh(question_attempt)

        # Update Game Session
        game_session.score = updated_score
        # Check if all questions have been answered
        total_questions = sum(len(cat.questions) for cat in game_session.quiz_board.categories)
        answered_questions = db.query(QuestionAttempt).filter(QuestionAttempt.game_session_id == game_session_id).count()
        if answered_questions == total_questions:
            game_session.status = "completed"
            game_session.completed_at = datetime.now()
        db.commit()
        db.refresh(game_session)

        response = AnswerQuestionResponse(
            question_id=question_id,
            status=status,
            correct_answer=question.answer_text,
            points_earned=points_earned,
            updated_score=updated_score,
            game_status=game_session.status
        )

        return response
