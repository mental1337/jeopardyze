from .game_session import (
    GameSessionResponse,
    SessionQuizBoardPyd,
    SessionCategoryPyd,
    SessionQuestionPyd,
    AnswerQuestionResponse,
    AnswerQuestionRequest
)

from .quiz_board import (
    TopQuizBoardModel,
    TopQuizBoardsResponse,
    QuestionPydanticModel,
    CategoryPydanticModel,
    QuizBoardPydanticModel
)

# This allows you to import directly from schemas like:
# from app.schemas import GameSessionResponse
# instead of:
# from app.schemas.game_session import GameSessionResponse

"""
This makes your imports cleaner in other files. For example:

# Without __init__.py exports
from app.schemas.game_session import GameSessionResponse, SessionQuizBoardPyd

# With __init__.py exports
from app.schemas import GameSessionResponse, SessionQuizBoardPyd
"""