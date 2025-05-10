from sqlalchemy import Column, ForeignKey, String, Integer
from app.models.base import MyBaseModel, Base
from sqlalchemy.orm import relationship

class Category(MyBaseModel):
    __tablename__ = "categories"
    
    name = Column(String, nullable=False)
    quiz_board_id = Column(Integer, ForeignKey("quiz_boards.id"), nullable=False)

    # Relationships
    quiz_board = relationship("QuizBoard", back_populates="categories")
    questions = relationship("Question", back_populates="category")
    